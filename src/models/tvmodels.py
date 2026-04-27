# Copyright (c) EEEM071, University of Surrey

import torch.nn as nn
import torchvision.models as tvmodels


__all__ = ["mobilenet_v3_small", "vgg16", "googlenet"]


class TorchVisionModel(nn.Module):
    def __init__(self, name, num_classes, loss, pretrained, **kwargs):
        super().__init__()

        self.loss = loss
        self.backbone = tvmodels.__dict__[name](pretrained=pretrained)
        # modified to handle both classifier and fc architecture attributes
        if hasattr(self.backbone, 'classifier'):
        # overwrite the classifier used for ImageNet pretrianing
        # nn.Identity() will do nothing, it's just a place-holder
            self.feature_dim = self.backbone.classifier[0].in_features
            self.backbone.classifier = nn.Identity()
        elif hasattr(self.backbone, 'fc'):
            self.feature_dim = self.backbone.fc.in_features
        # Overwrite the fc layer used for ImageNet pretraining
            self.backbone.fc = nn.Identity()
        else: 
            raise AttributeError(f"Model {name} has an unsupported architecture.")
        
        self.classifier = nn.Linear(self.feature_dim, num_classes)

    def forward(self, x):
        v = self.backbone(x)

        if not self.training:
            return v

        y = self.classifier(v)

        if self.loss == {"xent"}:
            return y
        elif self.loss == {"xent", "htri"}:
            return y, v
        else:
            raise KeyError(f"Unsupported loss: {self.loss}")


def vgg16(num_classes, loss={"xent"}, pretrained=True, **kwargs):
    model = TorchVisionModel(
        "vgg16",
        num_classes=num_classes,
        loss=loss,
        pretrained=pretrained,
        **kwargs,
    )
    return model


def mobilenet_v3_small(num_classes, loss={"xent"}, pretrained=True, **kwargs):
    model = TorchVisionModel(
        "mobilenet_v3_small",
        num_classes=num_classes,
        loss=loss,
        pretrained=pretrained,
        **kwargs,
    )
    return model

def googlenet(num_classes, loss={"xent"}, pretrained=True, **kwargs):
    model = TorchVisionModel(
        "googlenet",
        num_classes=num_classes,
        loss=loss,
        pretrained=pretrained,
        **kwargs,
    )
    return model


# Define any models supported by torchvision bellow
# https://pytorch.org/vision/0.11/models.html
