
import pandas as pd
from plotnine import *

data = pd.DataFrame({
  'x': [2,3,45,6,3,2,34,24,5,6,7 ]
})


data.x

( ggplot() + geom_histogram(data = data, mapping = aes(x = 'x')) )
