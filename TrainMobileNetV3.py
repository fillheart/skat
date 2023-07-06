# %% [markdown]
# # Обучение `MobileNetV3 small` на распознавание армянских букв
# 
# Основной код обучения взят из примера pytorch
# https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
# 
# Загружается mobilenetv3 small и обучается на простой выборке `simpledataset`

# %%
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
from PIL import Image
from tempfile import TemporaryDirectory
torch.cuda.empty_cache()

# %% [markdown]
# Подготовка обучающей выборки (созданной ранее)

# %%
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ]),
    'test': transforms.Compose([
        transforms.ToTensor()
    ]),
}

data_dir = '../dataset/simpledataset/'
image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                          data_transforms[x])
                  for x in ['train', 'test']}



dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                             shuffle=True, num_workers=4)
              for x in ['train', 'test']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}
class_names = image_datasets['train'].classes

device = torch.device("cuda:0")

# %% [markdown]
# Отображение части выборки


# %% [markdown]
# Функция обучения модели

# %%
def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
    since = time.time()

    # Create a temporary directory to save training checkpoints
    with TemporaryDirectory() as tempdir:
        best_model_params_path = os.path.join(tempdir, 'best_model_params.pt')

        torch.save(model.state_dict(), best_model_params_path)
        best_acc = 0.0

        for epoch in range(num_epochs):
            print(f'Epoch {epoch}/{num_epochs - 1}')
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in ['train', 'test']:
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()



                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

                # deep copy the model
                if phase == 'test' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    torch.save(model.state_dict(), best_model_params_path)

            print()

        time_elapsed = time.time() - since
        print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        print(f'Best val Acc: {best_acc:4f}')

        # load best model weights
        model.load_state_dict(torch.load(best_model_params_path))
    return model

# %% [markdown]
# Загрузка готовой модели MobileNetV3 small с предобученными параметрами

# %%
modelMobileNet = models.mobilenet_v3_small(weights='IMAGENET1K_V1')

# так как другая классификация, чем в готовой модели, то замена на свои слои
newClassifier = nn.Sequential(
    nn.Linear(in_features=576, out_features=1024, bias=True),
    nn.Hardswish(),
    nn.Dropout(p=0.2, inplace=True),
    nn.Linear(in_features=1024, out_features=34, bias=True)
  )

modelMobileNet.classifier = newClassifier

# перенос модели для выполнения и обучения на видеокарту (если доступна)
modelMobileNet = modelMobileNet.to(device)

# функция потерь, стандартная для обучения классификации
criterion = nn.CrossEntropyLoss()

# Выбор параметров для обучения
# параметры всей сети
# optimizer_ft = optim.SGD(model_ft.classifier.parameters(), lr=0.01, momentum=0.9)
optimizer = optim.Adam(modelMobileNet.classifier.parameters(), lr=0.001)

# параметры только последнего слоя. 
# Так как имеется предобученная модель нейронной сети, то промежуточные слои уже обучены выделять важные признаки из изображений. 
# По этой причине можно выполнять обучение только замененных слоев, отвечающих за классификацию, что позволяет ускорить обучение.
# Я не уверен что это тут будет работать
# optimizer = optim.Adam(modelMobileNet.classifier.parameters(), lr=0.001)

# уменьшение скорости обучения в 10 раза каждый 30 эпох
exp_lr_scheduler = lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)



# %% [markdown]
# Обучение модели

if __name__ == '__main__':
    modelMobileNet = train_model(modelMobileNet, criterion, optimizer, exp_lr_scheduler, num_epochs=100)
    # num_epochs - количество эпох обучения