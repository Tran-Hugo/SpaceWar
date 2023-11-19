import pygame
import os
import uuid

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.uuid = str(uuid.uuid4())
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(os.path.join("assets/explosions/", "exp"+str(num)+".png"))
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()
	
	def to_dict(self):
		return {
			"uuid": self.uuid,
			"x": self.rect.x,
			"y": self.rect.y
		}
	
	def from_dict(self, data):
		self.uuid = data["uuid"]
		self.rect.x = data["x"]
		self.rect.y = data["y"]