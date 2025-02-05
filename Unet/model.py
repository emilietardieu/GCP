import torch.nn as nn
import torch.nn.functional as F
import torch

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        
        # ENCODEUR
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1), # 256x256
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2) # 256x256->128x128
        )
        # BOTTLENECK
        self.bottleneck = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, padding=1), # 128x128
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 128x128->64x64 
        )

        # DÉCODEUR
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=2, stride=2), # 64x64->128x128
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 16, kernel_size=3, padding=1), 
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(16, 8, kernel_size=2, stride=2), # 128x128->256x256
            nn.ReLU(inplace=True), 
            nn.Conv2d(8, 8, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 1, kernel_size=1) 
        )
        
        self.fc = nn.Linear(256 * 256, 2)
        
        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.modules(): # Parcours de tous les modules du réseau
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d): # Si le module est une couche de convolution ou de déconvolution 
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu') # Initialisation des poids avec la méthode de Kaiming He
                if m.bias is not None: # Si le module possède un biais
                    nn.init.constant_(m.bias, 0) # Initialisation du biais à 0
            elif isinstance(m, nn.Linear): # Si le module est une couche linéaire
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu') # Initialisation des poids avec la méthode de Kaiming He
                nn.init.constant_(m.bias, 0) # Initialisation du biais à 0

    def forward(self, x):
        # Encoder
        x = self.encoder(x)
        
        # Bottleneck
        x = self.bottleneck(x)
        
        # Decoder
        x = self.decoder(x)
        
        # Flatten
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        return x



