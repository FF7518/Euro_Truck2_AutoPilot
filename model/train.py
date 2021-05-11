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


train_loader = load_data('../EuroTruck_v6_highway_small.npy')
test_loader = load_data('../EuroTruck_v6_highway_test.npy')

model = EuroTruckModel().to(device)
optimizer = torch.optim.SGD(model.parameters(), lr=1e-2, momentum=0.5)
criterion = torch.nn.CrossEntropyLoss()


def train(epoch):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        # print(data)
        img = data['image']
        target = data['label']
        img = torch.unsqueeze(img, 1)
        img = img.float() / 255.0
        # target = target.float()

        img, target = img.to(device), target.to(device)
        optimizer.zero_grad()

        # forward + backward + update
        output = model(img)
        # print(type(target[0]))

        loss = criterion(output, target)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 3 == 2 :
            print('[第%d轮迭代, batch=%5d] loss: %.3f' % (epoch+1, batch_idx+1, running_loss / 2000))
            running_loss = 0.0


def test():
    print('test--------------------')
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            img = data['image']
            target = data['label']

            img = torch.unsqueeze(img, 1)
            img = img.float() / 255.0
            # target = target.float()

            output = model(img)

            print(output.data)


if __name__ == '__main__':
    for epoch in range(5):
        train(epoch)
        test()