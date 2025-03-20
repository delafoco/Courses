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
        self.history_fine = None
        
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
    
    def prepare_data(self, train_dir, validation_dir, test_dir=None, batch_size=32):
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
        
        # Normalisation pour la validation et le test
        validation_datagen = ImageDataGenerator(rescale=1./255)
        
        # Création des générateurs de données
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.input_shape,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=self.input_shape,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        test_generator = None
        if test_dir:
            test_datagen = ImageDataGenerator(rescale=1./255)
            test_generator = test_datagen.flow_from_directory(
                test_dir,
                target_size=self.input_shape,
                batch_size=batch_size,
                class_mode='categorical',
                shuffle=False
            )
        
        return train_generator, validation_generator, test_generator
    
    def train(self, train_generator, validation_generator, epochs=20, steps_per_epoch=100):
        # Callbacks pour la sauvegarde du meilleur modèle
        checkpoint = ModelCheckpoint(
            'best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        )
        
        # Early stopping pour éviter le surapprentissage
        early_stopping = EarlyStopping(
            monitor='val_loss',
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
            validation_steps=50,
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
        plt.plot(self.history.history['val_accuracy'], label='Précision (validation)')
        plt.title('Précision du modèle')
        plt.xlabel('Époque')
        plt.ylabel('Précision')
        plt.legend()
        
        # Courbe de perte
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['loss'], label='Perte (train)')
        plt.plot(self.history.history['val_loss'], label='Perte (validation)')
        plt.title('Perte du modèle')
        plt.xlabel('Époque')
        plt.ylabel('Perte')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.close()
    
    def evaluate_model(self, test_generator):
        """Évalue le modèle sur l'ensemble de test"""
        if test_generator is None:
            print("Aucun ensemble de test fourni")
            return
            
        # Évaluation
        results = self.model.evaluate(test_generator)
        print("\nRésultats sur l'ensemble de test:")
        print(f"Perte: {results[0]:.4f}")
        print(f"Précision: {results[1]:.4f}")
        print(f"Précision (métrique): {results[2]:.4f}")
        print(f"Rappel: {results[3]:.4f}")
        
        # Prédictions
        predictions = self.model.predict(test_generator)
        y_pred = np.argmax(predictions, axis=1)
        y_true = test_generator.classes
        
        # Matrice de confusion
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Matrice de confusion')
        plt.ylabel('Valeur réelle')
        plt.xlabel('Valeur prédite')
        plt.savefig('confusion_matrix.png')
        plt.close()
        
        # Rapport de classification
        class_names = list(test_generator.class_indices.keys())
        report = classification_report(y_true, y_pred, target_names=class_names)
        print("\nRapport de classification:")
        print(report)
        
        # Sauvegarder le rapport
        with open('classification_report.txt', 'w') as f:
            f.write(report)
    
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
    # Exemple d'utilisation
    trainer = MushroomTrainer(num_classes=5)  # Pour 5 types de champignons
    
    # Préparation des données
    train_generator, validation_generator, test_generator = trainer.prepare_data(
        train_dir='data/train',
        validation_dir='data/validation',
        test_dir='data/test'
    )
    
    # Premier entraînement (couches de base gelées)
    trainer.history = trainer.train(train_generator, validation_generator)
    
    # Fine-tuning (débloquer les dernières couches)
    trainer.unfreeze_layers()
    trainer.model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    # Deuxième entraînement (fine-tuning)
    trainer.history_fine = trainer.train(train_generator, validation_generator, epochs=10)
    
    # Visualisation de l'historique
    trainer.plot_training_history()
    
    # Évaluation sur l'ensemble de test
    trainer.evaluate_model(test_generator)
    
    # Sauvegarde du modèle
    trainer.save_model()

if __name__ == "__main__":
    main() 