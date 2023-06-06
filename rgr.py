import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import math

# импортируем изображение
img = cv2.imread('D:/Python/1.jpg', cv2.IMREAD_GRAYSCALE) #я 18 вариант. Фото прикрепил с заданием

np.set_printoptions(threshold=sys.maxsize)

plt.imshow(img, cmap='gray')

# берем первую строку из картинки, чтобы преобразовать в сигнал
img2 = img[1]

# удаляем незначащие 0 (квадратик с номером варианта)
img2 = np.delete(img2, np.where(img2 == 0))

# функция расшифровки
def show(image):
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)

  major_ticksx = np.arange(0, 1001, 100)
  minor_ticksx = np.arange(0, 1001, 20)
  major_ticksy = np.arange(0, 251, 50)
  minor_ticksy = np.arange(0, 251, 10)

  ax.set_xticks(major_ticksx)
  ax.set_xticks(minor_ticksx, minor=True)
  ax.set_yticks(major_ticksy)
  ax.set_yticks(minor_ticksy, minor=True)

  # Add grid
  ax.grid(which='both')

  # Or if you want different settings for the grids:
  ax.grid(which='minor', alpha=0.2)
  ax.grid(which='major', alpha=0.5)

  ax.plot(image)

  plt.show()


# фильтр скользящего среднего
def s_middle(y, n):
  # при первом вызове создаем переменные
  if 'y_stack' not in s_middle.__dict__:
    s_middle.y_stack = np.zeros(n)
  if 'k' not in s_middle.__dict__:
   s_middle.k = 0
  # если размер стека нужно изменить
  if n != s_middle.y_stack.shape[0]:
   s_middle.y_stack = np.zeros(n)
  s_middle.k += 1
  if s_middle.k >= n:
    s_middle.k = 0
  # Циклическая перезапись
  s_middle.y_stack[s_middle.k] = y
  return np.sum(s_middle.y_stack) / n


# медианный фильтр
def median(y, n):
  # при первом вызове создаем переменные
  if n < 3: n = 3
  if 'y_stack' not in median.__dict__:
    median.y_stack = np.zeros(n)
  if 'k' not in median.__dict__:
    median.k = 0
  # если размер стека нужно изменить
  if n != median.y_stack.shape[0]:
    median.y_stack = np.zeros(n)
  median.k += 1
  if median.k >= n:
    median.k = 0
  median.y_stack[median.k] = y
  rez = np.sum(median.y_stack)
  rez = rez - max(median.y_stack) - min(median.y_stack)
  rez = rez / (n-2)
  return rez


def sin(x):
  a = 25
  b = 100
  c = 60
  return (a * math.sin(3.14*b*x/5000)+c)


img3 = np.zeros(1000)
j = 0
for i in img2:
  img3[j]=s_middle(i, 30)
  j = j+1

j = 0
img4 = np.zeros(1000)
for i in img3:
  img4[j]=median(i, 15)
  j = j+1

show (img4[29:])


sin_array = np.zeros(1000)
for i in range(1000):
  sin_array[i] = sin(i)


consin = np.convolve(img4, sin_array, mode='full')
plt.plot(consin)
plt.show()
