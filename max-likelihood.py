import numpy as np
import pandas as pd
from scipy import optimize
import random


#似然函数
def likelihood(M, ps, pu):
    return np.prod(1 - (1 - ps) ** M) * np.prod((1 - pu) ** M)


#极大似然函数
def max_likelihood(ps, pu):
    return np.argmax(np.array([likelihood(m, ps, pu) for m in range(0, 5000000, 500)])) * 500


#利用scipy.optimize方法计算极大似然函数的最值
def scipy_max_likelihood(ps, pu):
    f = lambda x: -likelihood(x, ps, pu)

    init_guess = 1 / (np.min(ps))

    return optimize.fmin(f, init_guess, disp=False)[0]


#定义一个类来表示词汇量估计过程
class VocabSizeEstimator:

    def __init__(self, corpus_path):

        print('Initializing...')

        #载入词汇表
        self.corpus = pd.read_csv(corpus_path, header=None)
        self.corpus.columns = ['word', 'freq']

        #提取表中单词的频率存入数组
        self.probs = np.array(self.corpus['freq'])

    #将测试结果存入boolean数组，估计m的大小
    def estimate_words_seen(self, sample: list[dict[str, any]], known: list[int], spicy_=False):

        sample_p = list(sample['freq'])
        s = np.array([x for x, y in zip(sample_p, known) if y])
        u = np.array([x for x, y in zip(sample_p, known) if not y])
        # print('s:',s)
        # print('u:', u)
        # print('int(scipy_max_likelihood(s,u))',int(scipy_max_likelihood(s,u)))
        # print('int(max_likelihood(s,u))', int(max_likelihood(s, u)))
        if spicy_:
            return int(scipy_max_likelihood(s, u))
        else:
            return int(max_likelihood(s, u))

    #计算词汇量
    def estimate_words_known_corpus(self, words_seen):

        s = np.vectorize(lambda x: (x - 1) * ((1 - x) ** words_seen - 1))
        # print('int(np.sum(s(self.probs)))',int(np.sum(s(self.probs))))
        return int(np.sum(s(self.probs)))

    def generate_sample(self, size, rare_threshold):

        rare_words = self.corpus[self.corpus['freq'] < rare_threshold]
        rows = random.sample(list(rare_words.index), size)
        return rare_words.loc[rows]

    #通过调用scipy函数来计算m的极大似然函数值，即最终结果词汇量
    def get_vocab_size(self, sample: list[dict[str, any]], known: list[int]):

        return self.estimate_words_known_corpus(self.estimate_words_seen(sample, known))

    def run(self):

        sample = self.generate_sample(20, 1e-3)

        K = []

        for i, word in enumerate(sample['word']):
            print(word)

            while True:

                know = input('Do you know this word y/n? ')

                if know == 'y':
                    K.append(1)
                    break
                elif know == 'n':
                    K.append(0)
                    break
                else:
                    continue

        print('OK, estimateing vocabulary size...')
        print('Your vocabulary size is ', self.get_vocab_size(sample, K))

    #传入随机生成的单词组计算词汇量
    def test(self, samples, labels):

        return self.get_vocab_size(samples, labels)


if __name__ == '__main__':
    # s = np.array([0.000001,0.001,0.0004,0.00001])
    # u = np.array([0.001])
    #
    # print(max_likelihood(s,u))
    # print()
    # print(scipy_max_likelihood(s,u))
    # VE = VocabSizeEstimator('corpus_corrected.csv')
    # len(VE.corpus)
    VE = VocabSizeEstimator('my_corpus.csv')
    VE.run()
