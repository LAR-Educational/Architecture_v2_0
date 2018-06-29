import time
from Modules import disattention

disattention.Th.load_classifier()

attention = disattention.Th(1)
attention.start()

closeAttention = disattention.Th(2)
closeAttention.start()

attention = disattention.Th(1)
attention.start()

closeAttention = disattention.Th(2)
closeAttention.start()

