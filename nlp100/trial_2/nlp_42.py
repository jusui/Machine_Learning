# coding: utf-8
import CaboCha
import pydotplus
import subprocess
from nlp_40 import *
"""
42. 係り元と係り先の文節の表示

係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．
ただし，句読点などの記号は出力しないようにせよ．
"""

class Chunk:
    
    def __init__(self, morphs: list, dst: str, srcs: str) -> None:
        """形態素(Morph object)のリスト(morphs), かかり先文節インデックス番号(dst),
        係り元文節インデックス番号のリスト(srcs)をメンバ変数に持つ"""

        self.morphs = morphs
        self.dst = int(dst.strip("D"))
        self.srcs = int(srcs)

    def join_morphs(self) -> str:
        """list morphs中の'記号'以外の各要素を結合して文字列を返す"""
        
        return ''.join([_morph.surface for _morph in self.morphs \
                        if _morph.pos != '記号'])

    def pair(self, sentence: list) -> str:
        return self.join_morphs() + '\t' + sentence[self.dst].join_morphs()
        
    def __str__(self) -> str:
        return 'srcs: {}, dst: {}, morphs: ({})'\
            .format( self.srcs,
                     self.dst,
                     '/'.join([str(_morph) for _morph in self.morphs]) )

    
def make_chunk_list(analyzed_file_name: str) -> list:
    """係り受け解析済みの文章ファイルを読み込んで，
    各文をChunkオブジェクトのリストとして表現"""

    sentences = []
    sentence  = []
    _chunk = None
    with open(analyzed_file_name, encoding = 'utf-8') as input_file:
        for line in input_file:
            line_list = line.split()
            if line_list[0] == '*':
                if _chunk is not None:
                    sentence.append(_chunk)
                _chunk = Chunk(morphs = [], dst = line_list[2], srcs = line_list[1])

            elif line_list[0] == 'EOS': # End of sentence
                if _chunk is not None:
                    sentence.append(_chunk)
                if len(sentence) > 0:
                    sentences.append(sentence)
                _chunk = None
                sentence = []
                
            else:
                line_list = line_list[0].split(',') + line_list[1].split(',')
                _morph = Morph(surface = line_list[0], base = line_list[7],
                               pos = line_list[1], pos1 = line_list[2])
                _chunk.morphs.append(_morph)

    return sentences

def is_valid_chunk(_chunk, sentence):
    return _chunk.join_morphs() != '' and _chunk.dst > -1 \
                                   and sentence[_chunk.dst].join_morphs() != ''


if __name__ == '__main__':

    chunked_sentences = make_chunk_list('neko.txt.cabocha')

    paired_sentences = [ [chunk.pair(sentence) for chunk in sentence \
                          if is_valid_chunk(chunk, sentence)] \
                         for sentence in chunked_sentences \
                         if len(sentence) > 1 ]
    
    print(paired_sentences[0:100])
        
