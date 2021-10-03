from panda3d.core import TextNode
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import aspect2d


class CustomTextNode():
    def __init__(self, name, text, pos, scale, loader):

        # directly make a text node to display text
        self.text = TextNode(name)
        self.text.set_text(text)
        text_node = aspect2d.attach_new_node(self.text)
        text_node.set_scale(scale)
        text_node.set_pos(pos)

        # import font and set pixels per unit font quality
        nunito_font = loader.load_font('media/fonts/Nunito/Nunito-Light.ttf')
        nunito_font.set_pixels_per_unit(100)
        nunito_font.set_page_size(512, 512)

        # apply default font
        self.text.set_font(nunito_font)

    # Update Text
    def updateText(self, text):
        self.text.setText(text)
