import io
import base64
from matplotlib import animation, rc
from IPython.display import HTML


filename = '~/DC.gif'

video = io.open(filename, 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<img src="data:image/gif;base64,{0}" type="gif" />'''.format(encoded.decode('ascii')))
