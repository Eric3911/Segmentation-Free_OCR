#!/usr/bin/env python
__author__ = 'solivr'
import time
import tensorflow as tf
from tensorflow.contrib.rnn import BasicLSTMCell, GRUCell
from .decoding import get_words_from_chars
from .config import Params, CONST
from .resnet import resnet

'''
使用tfrecords训练图片所使用
'''


def weightVar(shape, mean=0.0, stddev=0.02, name='weights'):
    init_w = tf.truncated_normal(shape=shape, mean=mean, stddev=stddev)
    return tf.Variable(init_w, name=name)


def biasVar(shape, value=0.0, name='bias'):
    init_b = tf.constant(value=value, shape=shape)
    return tf.Variable(init_b, name=name)


def conv2d(input, filter, strides=[1, 1, 1, 1], padding='SAME', name=None):
    return tf.nn.conv2d(input, filter, strides=strides, padding=padding, name=name)


def deep_cnn(input_imgs: tf.Tensor, is_training: bool, params: Params, summaries: bool = True) -> tf.Tensor:
    '''
    对输入图像进行卷积操作
    :param input_imgs: 输入如下 tensor类型 128*32*304*3
    :param is_training: 是否是训练阶段
    :param summaries: 是否显示在tensorboard中
    :return:
    '''
    # 取出输入图像通道
    input_imgs = tf.reshape(input_imgs, [-1, params.input_shape[0], params.input_shape[1], params.image_channels])
    input_tensor = input_imgs

    if input_tensor.shape[-1] == 1:
        input_channels = 1
    elif input_tensor.shape[-1] == 3:
        input_channels = 3
    else:
        raise NotImplementedError

    # Following source code, not paper

    with tf.variable_scope('deep_cnn'):
        # - conv1 128*32*304*3 -> 128*32*304*64
        # - maxPool2x2 128*32*304*64 -> 128*16*152*64
        with tf.variable_scope('layer1'):
            W = weightVar([3, 3, input_channels, 64])
            b = biasVar([64])
            conv = conv2d(input_tensor, W, name='conv')
            out = tf.nn.bias_add(conv, b)
            conv1 = tf.nn.relu(out)
            pool1 = tf.nn.max_pool(conv1, [1, 2, 2, 1], strides=[1, 2, 2, 1],
                                   padding='SAME', name='pool')

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer1/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer1/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv2  128*16*152*64 -> 128*16*152*128
        # - maxPool 2x2  128*16*152*128 -> 128*8*76*128
        with tf.variable_scope('layer2'):
            W = weightVar([3, 3, 64, 128])
            b = biasVar([128])
            conv = conv2d(pool1, W)
            out = tf.nn.bias_add(conv, b)
            conv2 = tf.nn.relu(out)
            pool2 = tf.nn.max_pool(conv2, [1, 2, 2, 1], strides=[1, 2, 2, 1],
                                   padding='SAME', name='pool1')

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer2/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer2/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv3 - w/batch-norm (as source code, not paper) 128*8*76*128 -> 128*8*76*256
        with tf.variable_scope('layer3'):
            W = weightVar([3, 3, 128, 256])
            b = biasVar([256])
            conv = conv2d(pool2, W)
            out = tf.nn.bias_add(conv, b)
            b_norm = tf.layers.batch_normalization(out, axis=-1,
                                                   training=is_training, name='batch-norm')
            conv3 = tf.nn.relu(b_norm, name='ReLU')

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer3/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer3/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv4 128*8*76*256 -> 128*8*76*256
        # - maxPool 2x1  128*8*76*256 -> 128*4*76*256
        with tf.variable_scope('layer4'):
            W = weightVar([3, 3, 256, 256])
            b = biasVar([256])
            conv = conv2d(conv3, W)
            out = tf.nn.bias_add(conv, b)
            conv4 = tf.nn.relu(out)
            pool4 = tf.nn.max_pool(conv4, [1, 2, 2, 1], strides=[1, 2, 1, 1],
                                   padding='SAME', name='pool4')

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer4/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer4/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv5 - w/batch-norm  128*4*76*256 -> 128*4*76*512
        with tf.variable_scope('layer5'):
            W = weightVar([3, 3, 256, 512])
            b = biasVar([512])
            conv = conv2d(pool4, W)
            out = tf.nn.bias_add(conv, b)
            b_norm = tf.layers.batch_normalization(out, axis=-1,
                                                   training=is_training, name='batch-norm')
            conv5 = tf.nn.relu(b_norm)

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer5/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer5/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv6  128*4*76*512 -> 128*4*76*512
        # - maxPool 2x1 (as source code, not paper) 128*4*76*512 -> 128*2*76*512
        with tf.variable_scope('layer6'):
            W = weightVar([3, 3, 512, 512])
            b = biasVar([512])
            conv = conv2d(conv5, W)
            out = tf.nn.bias_add(conv, b)
            conv6 = tf.nn.relu(out)
            pool6 = tf.nn.max_pool(conv6, [1, 2, 2, 1], strides=[1, 2, 1, 1],
                                   padding='SAME', name='pool6')

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer6/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer6/bias:0'][0]
                tf.summary.histogram('bias', bias)

        # - conv 7 - w/batch-norm (as source code, not paper) 128*2*76*512 -> 128*1*75*512
        with tf.variable_scope('layer7'):
            W = weightVar([2, 2, 512, 512])
            b = biasVar([512])
            conv = conv2d(pool6, W, padding='VALID')
            out = tf.nn.bias_add(conv, b)
            b_norm = tf.layers.batch_normalization(out, axis=-1,
                                                   training=is_training, name='batch-norm')
            conv7 = tf.nn.relu(b_norm)

            if summaries:
                weights = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer7/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables() if var.name == 'deep_cnn/layer7/bias:0'][0]
                tf.summary.histogram('bias', bias)

        cnn_net = conv7
        # reshape 特征图
        with tf.variable_scope('Reshaping_cnn'):
            shape = cnn_net.get_shape()  # [batch, height, width, features]
            # [batch, width, height, features] 128*1*75*512 -> 128*75*1*512
            transposed = tf.transpose(cnn_net, perm=[0, 2, 1, 3], name='transposed')
            # [batch, width, height x features] 128*75*1*512 -> 128*75*512
            conv_reshaped = tf.reshape(transposed, [-1, shape[2], shape[1] * shape[3]], name='reshaped')

    return conv_reshaped


def deep_bidirectional_lstm(inputs: tf.Tensor, params: Params, summaries: bool = True) -> tf.Tensor:
    # Prepare data shape to match `bidirectional_rnn` function requirements
    # Current data input shape: (batch_size, n_steps, n_input) "(batch, time, height)"

    list_n_hidden = [256, 256]

    with tf.name_scope('deep_bidirectional_lstm'):
        # # Forward direction cells
        fw_cell_list = [BasicLSTMCell(nh, forget_bias=1.0) for nh in list_n_hidden]
        # # Backward direction cells
        bw_cell_list = [BasicLSTMCell(nh, forget_bias=1.0) for nh in list_n_hidden]
        # Forward direction cells
        # fw_cell_list = [GRUCell(nh) for nh in list_n_hidden]
        # Backward direction cells
        # bw_cell_list = [GRUCell(nh) for nh in list_n_hidden]

        lstm_net, _, _ = tf.contrib.rnn.stack_bidirectional_dynamic_rnn(fw_cell_list,
                                                                        bw_cell_list,
                                                                        inputs,
                                                                        dtype=tf.float32
                                                                        )

        # Dropout layer
        lstm_net = tf.nn.dropout(lstm_net, keep_prob=params.keep_prob_dropout)

        with tf.variable_scope('Reshaping_rnn'):
            shape = lstm_net.get_shape().as_list()  # [batch, width, 2*n_hidden]
            rnn_reshaped = tf.reshape(lstm_net, [-1, shape[-1]])  # [batch x width, 2*n_hidden]  128*75*512->9600*512

        with tf.variable_scope('fully_connected'):  # 9600*512 -> 9600*3851
            W = weightVar([list_n_hidden[-1] * 2, params.n_classes])
            b = biasVar([params.n_classes])
            fc_out = tf.nn.bias_add(tf.matmul(rnn_reshaped, W), b)

            if summaries:
                weights = [var for var in tf.global_variables()
                           if var.name == 'deep_bidirectional_lstm/fully_connected/weights:0'][0]
                tf.summary.histogram('weights', weights)
                bias = [var for var in tf.global_variables()
                        if var.name == 'deep_bidirectional_lstm/fully_connected/bias:0'][0]
                tf.summary.histogram('bias', bias)
        # 9600*3851 -> 128*75*3851
        lstm_out = tf.reshape(fc_out, [-1, inputs.shape[1], params.n_classes],
                              name='reshape_out')  # [batch, width, n_classes]
        raw_pred = tf.argmax(tf.nn.softmax(lstm_out), axis=2, name='raw_prediction')

        # Swap batch and time axis 128*75*3851->75*128*3851
        lstm_out = tf.transpose(lstm_out, [1, 0, 2], name='transpose_time_major')  # [width(time), batch, n_classes]

        return lstm_out, raw_pred


def crnn_fn(features, labels, mode, params):
    """
    :param features: dict {
                            'images'
                            'images_widths'
                            'filenames'
                            }
    :param labels: labels. flattend (1D) array with encoded label (one code per character)
    :param mode:
    :param params: dict {
                            'Params'
                        }
    :return:
    """

    parameters = params.get('Params')
    # 如果不是Params类型，报错
    assert isinstance(parameters, Params)
    # 设置训练和其他阶段的dropout比例
    if mode == tf.estimator.ModeKeys.TRAIN:
        parameters.keep_prob_dropout = 0.7
    else:
        parameters.keep_prob_dropout = 1.0
    # 开始执行网络-cnn阶段  128*32*304*3 -> 128*75*512
    conv = deep_cnn(features['images'], (mode == tf.estimator.ModeKeys.TRAIN), params=parameters, summaries=False)
    # conv = resnet(features['images'], (mode == tf.estimator.ModeKeys.TRAIN), summaries=False)
    # rnn阶段 128*75*512 -> 75*128*3851
    logprob, raw_pred = deep_bidirectional_lstm(conv, params=parameters, summaries=False)
    # 计算图片宽度
    n_pools = CONST.DIMENSION_REDUCTION_W_POOLING  # 2x2 pooling in dimension W on layer 1 and 2
    # seq_len_inputs是输入到rnn图像的长度，在deep_cnn中，宽度减少了input_w/*/4 -1
    seq_len_inputs = tf.divide(features['images_widths'], n_pools, name='seq_len_input_op') - 1
    # 构造输出词典
    predictions_dict = {'prob': logprob,
                        'raw_predictions': raw_pred,
                        }
    try:
        predictions_dict['filenames'] = features['filenames']
    except KeyError:
        pass

    if not mode == tf.estimator.ModeKeys.PREDICT:
        # Convert string label to code label 将字符串label转换成数字label，即，每个数字在字母表中的索引

        #  ************************************* start  *************************************
        #  当前tensorflow版本的string_split不支持utf8字符，采取一种折中方案，保存标签的时候就保存为索引，以'$'分隔
        # 待支持后将下面代码解禁
        # keys = [c for c in parameters.alphabet]
        # values = parameters.alphabet_codes
        #
        # # Convert string label to code label
        # with tf.name_scope('str2code_conversion'):
        #     table_str2int = tf.contrib.lookup.HashTable(tf.contrib.lookup.KeyValueTensorInitializer(keys, values), -1)
        #     splited = tf.string_split(labels, delimiter='')  # TODO change string split to utf8 split in next tf version
        #     codes = table_str2int.lookup(splited.values)
        #     sparse_code_target = tf.SparseTensor(splited.indices, codes, splited.dense_shape)
        # ************************************* end  ****************************************


        # ************临时解决方案的代码 -start****************************************************************************
        with tf.name_scope('str2code_conversion'):
            splited = tf.string_split(labels, delimiter='$')
            sparse_code_target = tf.SparseTensor(splited.indices,
                                                 tf.cast(tf.string_to_number(splited.values), tf.int32),
                                                 splited.dense_shape)

        seq_lengths_labels = tf.bincount(tf.cast(sparse_code_target.indices[:, 0], tf.int32),
                                         minlength=tf.shape(predictions_dict['prob'])[1])
        # ************临时解决方案的代码-end*******************************************************************************

        # 开始计算Loss
        # ----
        # >>> Cannot have longer labels than predictions -> error
        with tf.control_dependencies(
                [tf.less_equal(sparse_code_target.dense_shape[1], tf.reduce_max(tf.cast(seq_len_inputs, tf.int64)))]):
            loss_ctc = tf.nn.ctc_loss(labels=sparse_code_target,
                                      inputs=predictions_dict['prob'],
                                      sequence_length=tf.cast(seq_len_inputs, tf.int32),
                                      preprocess_collapse_repeated=False,
                                      ctc_merge_repeated=True,
                                      ignore_longer_outputs_than_inputs=True,
                                      # returns zero gradient in case it happens -> ema loss = NaN
                                      time_major=True)
            loss_ctc = tf.reduce_mean(loss_ctc)
            loss_ctc = tf.Print(loss_ctc, [loss_ctc], message='* Loss : ')

        global_step = tf.train.get_or_create_global_step()
        # 创建一个学习率指数衰减器
        ema = tf.train.ExponentialMovingAverage(decay=0.99, num_updates=global_step, zero_debias=True)
        # Create the shadow variables, and add op to maintain moving averages
        maintain_averages_op = ema.apply([loss_ctc])
        loss_ema = ema.average(loss_ctc)

        # 创建一个Train op 并且制定优化策略
        # --------
        learning_rate = tf.train.exponential_decay(parameters.learning_rate, global_step,
                                                   parameters.learning_decay_steps, parameters.learning_decay_rate,
                                                   staircase=True)

        if parameters.optimizer == 'ada':
            optimizer = tf.train.AdadeltaOptimizer(learning_rate)
        elif parameters.optimizer == 'adam':
            optimizer = tf.train.AdamOptimizer(learning_rate, beta1=0.5)
        elif parameters.optimizer == 'rms':
            optimizer = tf.train.RMSPropOptimizer(learning_rate)

        update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        opt_op = optimizer.minimize(loss_ctc, global_step=global_step)
        with tf.control_dependencies(update_ops + [opt_op]):
            train_op = tf.group(maintain_averages_op)

        # 写入tensorboard Summaries
        # ---------

        tf.summary.scalar('learning_rate', learning_rate)
        tf.summary.scalar('losses/ctc_loss', loss_ctc)
    else:
        loss_ctc, train_op = None, None

    if mode in [tf.estimator.ModeKeys.EVAL, tf.estimator.ModeKeys.PREDICT, tf.estimator.ModeKeys.TRAIN]:
        # 将预测的label转换为字符
        with tf.name_scope('code2str_conversion'):
            # 构造hash表
            keys = tf.cast(parameters.alphabet_decoding_codes, tf.int64)
            values = [c for c in parameters.alphabet_decoding]
            table_int2str = tf.contrib.lookup.HashTable(tf.contrib.lookup.KeyValueTensorInitializer(keys, values), '?')

            sparse_code_pred, log_probability = tf.nn.ctc_beam_search_decoder(predictions_dict['prob'],
                                                                              sequence_length=tf.cast(seq_len_inputs,
                                                                                                      tf.int32),
                                                                              merge_repeated=False,
                                                                              beam_width=100,
                                                                              top_paths=2)
            # Score
            predictions_dict['score'] = tf.subtract(log_probability[:, 0], log_probability[:, 1])
            # around 10.0 -> seems pretty sure, less than 5.0 bit unsure, some errors/challenging images
            sparse_code_pred = sparse_code_pred[0]

            sequence_lengths_pred = tf.bincount(tf.cast(sparse_code_pred.indices[:, 0], tf.int32),
                                                minlength=tf.shape(predictions_dict['prob'])[1])

            pred_chars = table_int2str.lookup(sparse_code_pred)
            predictions_dict['words'] = get_words_from_chars(pred_chars.values, sequence_lengths=sequence_lengths_pred)

            tf.summary.text('predicted_words', predictions_dict['words'][:10])
    # 计算训练准确率
    if mode == tf.estimator.ModeKeys.TRAIN:
        # with tf.name_scope('train-evaluation'):
        CER = tf.metrics.mean(tf.edit_distance(sparse_code_pred, tf.cast(sparse_code_target, dtype=tf.int64)),
                              name='CER')
        # Convert label codes to decoding alphabet to compare predicted and groundtrouth words
        target_chars = table_int2str.lookup(tf.cast(sparse_code_target, tf.int64))
        target_words = get_words_from_chars(target_chars.values, seq_lengths_labels)

        accuracy = tf.metrics.accuracy(target_words, predictions_dict['words'], name='accuracy')

        CER = tf.Print(CER, [CER], message='-- train CER : ')
        accuracy = tf.Print(accuracy, [accuracy], message='-- train Accuracy : ')
        tf.summary.scalar('train_accuracy', accuracy[1])

    # Evaluation ops
    # --------------
    if mode == tf.estimator.ModeKeys.EVAL:
        with tf.name_scope('evaluation'):
            CER = tf.metrics.mean(tf.edit_distance(sparse_code_pred, tf.cast(sparse_code_target, dtype=tf.int64)),
                                  name='CER')
            # Convert label codes to decoding alphabet to compare predicted and groundtrouth words
            target_chars = table_int2str.lookup(tf.cast(sparse_code_target, tf.int64))
            target_words = get_words_from_chars(target_chars.values, seq_lengths_labels)
            accuracy = tf.metrics.accuracy(target_words, predictions_dict['words'], name='accuracy')
            eval_metric_ops = {
                'eval/accuracy': accuracy,
                'eval/CER': CER,
            }

            CER = tf.Print(CER, [CER], message='-- val CER : ')
            accuracy = tf.Print(accuracy, [accuracy], message='--val Accuracy : ')
    else:
        eval_metric_ops = None

    # 需要输出的op
    export_outputs = {'predictions': tf.estimator.export.PredictOutput(predictions_dict)}

    return tf.estimator.EstimatorSpec(
        mode=mode,
        predictions=predictions_dict,
        loss=loss_ctc,
        train_op=train_op,
        eval_metric_ops=eval_metric_ops,
        export_outputs=export_outputs,
        scaffold=tf.train.Scaffold()
        # scaffold=tf.train.Scaffold(init_fn=None)  # Specify init_fn to restore from previous model
    )
