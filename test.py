players, hand_size = input().split()
cards = input().split()
print(cards)
while True:
	movetype = input()
	if movetype == "PLAY":
		trank = input()
		cards = input().split()
		print(cards[0])
	elif movetype == "BS":
		print(1)