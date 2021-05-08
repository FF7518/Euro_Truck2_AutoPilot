# -*- encoding: utf-8 -*-
"""
@File    :   train.py    

@Time             @Author    @Version    @Description
------------      -------    --------    -----------
2021/5/8 13:44   FF7518     1.0         None
"""
from data import load_data
import torch
from model import EuroTruckModel, device


et = load_data('../EuroTruck_v6_highway_small.npy')

model = EuroTruckModel(n_speed_classes=2, n_turn_classes=2).to(device)
optimizer = torch.optim.RMSprop(model.parameters(), lr=1e-2)
criterion = torch.nn.CrossEntropyLoss()

def train(epoch=2):
    running_loss = 0.0
    for batch_idx, data in enumerate(et, 0):
        img = data['image']
        img = torch.unsqueeze(img, 1)
        img = img.float() / 255.0
        print(img[0])
        target = data['label']
        img, speed_target = img.to(device), target.to(device)
        optimizer.zero_grad()

        #       # forward + backward + update
        output = model(img)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 1 == 0 :
            print('[%d, %5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss / 2000))
            running_loss = 0.0


if __name__ == '__main__':
    train()