import random

names = ('Joseph'), ('Jordan'), ('LeRoy'), ('Zack'), ('Joshua'), ('Marcus'), ('Tommy'), ('Randy'), ('Josh'), ('Johnny')
verbs = ('ran'), ('walked'), ('hid'), ('drank'), ('flew'), ('advised'), ('strangled'), ('suffered'), ('awoke'), ('killed')

for item in names:
    print ("%s was naughty, they %s today." % (item, random.choice(verbs)))

