import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

class MushroomTrainer:
    def __init__(self, num_classes, input_shape=(224, 224)):
        self.num_classes = num_classes
        self.input_shape = input_shape
        self.model = self.build_model()
        self.history = None
        
    def build_model(self):
        # Charger le modèle ResNet50 pré-entraîné
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=self.input_shape + (3,))
        
        # Congeler les couches du modèle de base
        base_model.trainable = False
        
        # Ajouter nos couches personnalisées
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)  # Pour éviter le surapprentissage
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Créer le modèle final
        model = Model(inputs=base_model.input, outputs=predictions)
        return model
    
    def prepare_data(self, train_dir, validation_dir=None, batch_size=32):
        # Augmentation des données pour l'entraînement
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Normalisation pour la validation
        validation_datagen = ImageDataGenerator(rescale=1./255)
        
        # Création des générateurs de données
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.input_shape,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        validation_generator = None
        if validation_dir:
            validation_generator = validation_datagen.flow_from_directory(
                validation_dir,
                target_size=self.input_shape,
                batch_size=batch_size,
                class_mode='categorical'
            )
        
        return train_generator, validation_generator
    
    def train(self, train_generator, validation_generator=None, epochs=20, steps_per_epoch=100):
        # Callbacks pour la sauvegarde du meilleur modèle
        checkpoint = ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy' if validation_generator else 'accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        )
        
        # Early stopping pour éviter le surapprentissage
        early_stopping = EarlyStopping(
            monitor='val_loss' if validation_generator else 'loss',
            patience=5,
            restore_best_weights=True
        )
        
        # Compilation du modèle
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        
        # Entraînement
        history = self.model.fit(
            train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=50 if validation_generator else None,
            callbacks=[checkpoint, early_stopping]
        )
        
        return history
    
    def plot_training_history(self):
        """Visualise l'historique d'entraînement"""
        if self.history is None:
            print("Aucun historique d'entraînement disponible")
            return
            
        plt.figure(figsize=(12, 4))
        
        # Courbe de précision
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['accuracy'], label='Précision (train)')
        if 'val_accuracy' in self.history.history:
            plt.plot(self.history.history['val_accuracy'], label='Précision (validation)')
        plt.title('Précision du modèle')
        plt.xlabel('Époque')
        plt.ylabel('Précision')
        plt.legend()
        
        # Courbe de perte
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['loss'], label='Perte (train)')
        if 'val_loss' in self.history.history:
            plt.plot(self.history.history['val_loss'], label='Perte (validation)')
        plt.title('Perte du modèle')
        plt.xlabel('Époque')
        plt.ylabel('Perte')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.close()
    
    def save_model(self, path='mushroom_model'):
        if not os.path.exists(path):
            os.makedirs(path)
        self.model.save(f'{path}/model.h5')
        print(f"Modèle sauvegardé dans {path}/model.h5")
    
    def unfreeze_layers(self, num_layers=30):
        """Débloque les dernières couches du modèle de base pour le fine-tuning"""
        for layer in self.model.layers[-num_layers:]:
            layer.trainable = True

def main():
    # Obtenir le nombre de classes (dossiers dans le dossier train)
    train_dir = os.path.join(os.path.dirname(__file__), 'data', 'train')
    num_classes = len([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    
    print(f"Nombre de classes détectées : {num_classes}")
    
    # Créer l'instance du trainer
    trainer = MushroomTrainer(num_classes=num_classes)
    
    # Préparer les données
    train_generator, validation_generator = trainer.prepare_data(
        train_dir=train_dir,
        validation_dir=None  # Pas de validation pour le moment
    )
    
    # Premier entraînement (couches de base gelées)
    trainer.history = trainer.train(
        train_generator=train_generator,
        validation_generator=validation_generator,
        epochs=20,
        steps_per_epoch=50
    )
    
    # Fine-tuning (débloquer les dernières couches)
    trainer.unfreeze_layers()
    trainer.model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    # Deuxième entraînement (fine-tuning)
    trainer.history = trainer.train(
        train_generator=train_generator,
        validation_generator=validation_generator,
        epochs=10,
        steps_per_epoch=50
    )
    
    # Visualisation de l'historique
    trainer.plot_training_history()
    
    # Sauvegarde du modèle
    trainer.save_model()

if __name__ == "__main__":
    main() 