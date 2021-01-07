import collections
import math
import random
import numpy as np
from six.moves import xrange
import os


def cut():
    In=open("训练语料.txt","r", encoding="utf-8")
    Words=[]
    List=[]
    a=0
    for Line in In:
        if(a<15000):    
            a+=1
            Line=Line.strip()
            Words.append(Line)
    
    with open('word2vec.txt', "w", encoding="UTF-8") as fW2V:
        for i in range(15000):
            fW2V.write(Words[i])
            fW2V.write('\n')

    In.close()

cut()


#一、加载数据集和处理
def preprocess():
    In=open("word2vec.txt","r", encoding="utf-8")
    Words=[]
    List=[]


    for Line in In:
        Line=Line.strip()
        List=Line.split(" ")
        for i in range(len(List)):
            Words.append(List[i])
        
    print(len(Words))       
    In.close()
    vocab=set(Words)
    length=len(vocab)
    em_list=[]
    print(length) 
    for index, every in enumerate(vocab):
        temp=[0]*(50+1)
        em_list.append(temp)
        em_list[index][0]=every
        #em_list[index][index+1]=1
    return em_list

words = preprocess()
print('Data size', len(words))


#建立一个词典，稀有的词用UNK  token（未知值来代替）
vocabulary_size = 100000
# words=words[0:200]
def build_dataset(words):
    # 词汇编码
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))#找到词频最大的前vocabulary_size个词，count中存储的是单词和数量
    print("count", len(count))

    dictionary = dict()
    #"给每个高频词一个编号
    for word, _ in count:
        dictionary[word] = len(dictionary)
    # 使用生产的词汇编码将前面产生的 string list[words] 转变成 num list[data]
    data = list()
    unk_count = 0
    for word in words:
        if word in dictionary:
            index = dictionary[word]
        else:
            index = 0#某个词不在高频词典中，索引值为0
            unk_count += 1#低频词数量加1
        data.append(index)#data和words对应，把词转换为下标
    count[0][1] = unk_count #低频词个数，都算同一个字符
    # 反转字典 key为词汇编码 values为词汇本身
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reverse_dictionary
#data只包含索引   count为高频词和对应数量   dictionary是高频词:索引     re....是字典的反转  索引:高频词   
data, count, dictionary, reverse_dictionary = build_dataset(words)
# #删除words节省内存
del words  
print('Most common words ', count[1:6])
print('Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]])

data_index = 0
# Step 3: Function to generate a training batch for the skip-gram model.
#为skip-gram模型产生一个batch训练样本
def generate_batch(batch_size, num_skips, skip_window):
    
    global data_index
    assert batch_size % num_skips == 0
    assert num_skips <= 2 * skip_window
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)#(1, batch_size)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)# (batch_size, 1)
    span = 2 * skip_window + 1  # [ left target right ]
    buffer = collections.deque(maxlen=span)#一个队列
    
    #遍历滑动窗口内的所有词语   左+中心词+右
    for _ in range(span):#依次取span个词放入buffer队列中
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data) # ?
#         print("buffer",buffer)   buffer deque([0, 0, 0], maxlen=3)
    print("除法:",batch_size//num_skips)
    for i in range(batch_size // num_skips):
        target = skip_window  # target label at the center of the buffer
        targets_to_avoid = [skip_window]
        for j in range(num_skips):
            while target in targets_to_avoid:
                target = random.randint(0, span - 1)
            targets_to_avoid.append(target)
            batch[i * num_skips + j] = buffer[skip_window]
            labels[i * num_skips + j, 0] = buffer[target]
        buffer.append(data[data_index])
        data_index = (data_index + 1) % len(data)
    return batch, labels
# 显示示例
batch, labels = generate_batch(batch_size=8, num_skips=2, skip_window=1)
print("batch:",batch)
print("lables",labels)
for i in range(8):
    print(batch[i], reverse_dictionary[batch[i]], '->', labels[i, 0], reverse_dictionary[labels[i, 0]])


# Step 4: Build and train a skip-gram model.
#构造模型
batch_size = 128
embedding_size = 100
skip_window = 1       
num_skips = 2         
valid_size = 4      
valid_window = 100  
num_sampled = 64    


with graph.as_default():
    # Input data.
    train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    valid_dataset = tf.constant(valid_examples, dtype=tf.int32)

    # 权重矩阵（也就是要被学习到的）
    embeddings = tf.Variable(
        tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
    # 选取张量embeddings中对应train_inputs索引的值
    embed = tf.nn.embedding_lookup(embeddings, train_inputs)

    # 转化变量输入，适配NCE
    nce_weights = tf.Variable(
        tf.truncated_normal([vocabulary_size, embedding_size],
                            stddev=1.0 / math.sqrt(embedding_size)))
    nce_biases = tf.Variable(tf.zeros([vocabulary_size]), dtype=tf.float32)

    # Compute the average NCE loss for the batch.
    # tf.nce_loss automatically draws a new sample of the negative labels each
    # time we evaluate the loss.
    loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights,
                                         biases=nce_biases, 
                                         inputs=embed, 
                                         labels=train_labels,
                                         num_sampled=num_sampled, 
                                         num_classes=vocabulary_size))

    # 优化器
    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)

    # 使用所学习的词向量来计算一个给定的 minibatch 与所有单词之间的相似度（余弦距离）
    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
    normalized_embeddings = embeddings / norm
    valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
    similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)

    # Add variable initializer.
    init = tf.global_variables_initializer()


# Step 5: Begin training.
num_steps = 5

with tf.Session(graph=graph) as session:
    # We must initialize all variables before we use them.
    init.run()
    print("Initialized")

    average_loss = 0
    for step in xrange(num_steps):
        batch_inputs, batch_labels = generate_batch(batch_size, num_skips, skip_window)
        feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}

        # We perform one update step by evaluating the optimizer op (including it
        # in the list of returned values for session.run()
        _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
        average_loss += loss_val

        if step % 2000 == 0:
            if step > 0:
                average_loss /= 2000
            # The average loss is an estimate of the loss over the last 2000 batches.
            print("Average loss at step ", step, ": ", average_loss)
            average_loss = 0

        # Note that this is expensive (~20% slowdown if computed every 500 steps)
        if step % 10000 == 0:
            sim = similarity.eval()
            for i in xrange(valid_size):
                valid_word = reverse_dictionary[valid_examples[i]]
                top_k = 8  # number of nearest neighbors
                nearest = (-sim[i, :]).argsort()[:top_k]
                log_str = "Nearest to %s:" % valid_word
                for k in xrange(top_k):
                    close_word = reverse_dictionary[nearest[k]]
                    log_str = "%s %s," % (log_str, close_word)
                print(log_str)
    final_embeddings = normalized_embeddings.eval()

# Step 6: 输出词向量
with open('vector.txt', "w", encoding="UTF-8") as fW2V:
    fW2V.write(str(vocabulary_size) + ' ' + str(embedding_size) + '\n')
    for i in xrange(final_embeddings.shape[0]):
        sWord = reverse_dictionary[i]
        sVector = ''
        for j in xrange(final_embeddings.shape[1]):
            sVector = sVector + ' ' + str(final_embeddings[i, j])
        fW2V.write(sWord + sVector + '\n')


embedding_file = './word2vec.txt'
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(embedding_file, binary=False)
print('Model loaded.')
