import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  
        std=[0.229, 0.224, 0.225])
])

def load_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)  
    return image


class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad = False
        self.resnet = nn.Sequential(*list(resnet.children())[:-1])  # remove last FC
        self.linear = nn.Linear(resnet.fc.in_features, embed_size)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.linear(features)
        return features


class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size):
        super(DecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        embeddings = self.embed(captions)
        inputs = torch.cat((features.unsqueeze(1), embeddings), 1)
        hiddens, _ = self.lstm(inputs)
        outputs = self.linear(hiddens)
        return outputs

    def generate(self, features, vocab, max_len=15):
        result = []
        states = None
        input = features.unsqueeze(1)

        for _ in range(max_len):
            hiddens, states = self.lstm(input, states)
            output = self.linear(hiddens.squeeze(1))
            predicted = output.argmax(1)
            result.append(predicted.item())
            input = self.embed(predicted).unsqueeze(1)
            if vocab[predicted.item()] == "<EOS>":
                break

        return [vocab[idx] for idx in result]


vocab = {
    0: "<PAD>",
    1: "<SOS>",
    2: "<EOS>",
    3: "a",
    4: "cat",
    5: "on",
    6: "mat",
    7: "dog",
    8: "sitting"
}
inv_vocab = {word: idx for idx, word in vocab.items()}
vocab_size = len(vocab)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

embed_size = 256
hidden_size = 512

encoder = EncoderCNN(embed_size).to(device)
decoder = DecoderRNN(embed_size, hidden_size, vocab_size).to(device)

image_path = "your_image.jpg"  # <-- change this to your image
image = load_image(image_path).to(device)

with torch.no_grad():
    features = encoder(image)

caption = decoder.generate(features, vocab)

print("Generated Caption: ", ' '.join(caption))
