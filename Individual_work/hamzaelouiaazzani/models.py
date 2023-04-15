from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input, Dense , Concatenate , Dropout , Lambda
from tensorflow.keras import backend as K
import tensorflow as tf



# Define the distance function for Siamese network
def euclidean_distance(vects):
    x, y = vects
    sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))

def model_without_ft():

    # Define input shape for rumor_input, user_input_name, and user_input_description
    input_shape = (768 , )

    # Create input layer with custom name for rumor_input
    rumor_input = Input(shape=input_shape, name='rumor_input')

    # Create input layer with custom name for user_input_name
    user_input_name = Input(shape=input_shape, name='user_input_name')

    # Create input layer with custom name for user_input_description
    user_input_description = Input(shape=input_shape, name='user_input_description')

    # Define input shape for user_inputnumeric
    input_shape_numeric = (2 , )

    # Create input layer with custom name for user_inputnumeric
    user_inputnumeric = Input(shape=input_shape_numeric, name='user_inputnumeric')

    #shared layer level 1
    shared_layer_1_1 = Dense(units=128, activation='sigmoid' , name='shared_layer_1_1')
    shared_layer_2_1 = Dense(units=128, activation='sigmoid', name='shared_layer_2_1')

    #shared layer level 2
    shared_layer_1_2 = Dense(units=32, activation='sigmoid' , name='shared_layer_1_2')
    shared_layer_2_2 = Dense(units=32, activation='sigmoid', name='shared_layer_2_2')

    #shared layer level 3
    shared_layer_1_3 = Dense(units=16, activation='sigmoid' , name='shared_layer_1_3')
    shared_layer_2_3 = Dense(units=16, activation='sigmoid', name='shared_layer_2_3')

    # Apply shared_layer_1_1 to rumor_input and user_input_name
    encoded_1 = shared_layer_1_1(rumor_input)
    encoded_2 = shared_layer_1_1(user_input_name) 

    # Apply shared_layer_2_1 to rumor_input and user_input_description
    encoded_3 = shared_layer_2_1(rumor_input)
    encoded_4 = shared_layer_2_1(user_input_description) 

    # Apply shared_layer_1_2 to encoded_1 and encoded_2
    encoded_5 = shared_layer_1_2(encoded_1)
    encoded_6 = shared_layer_1_2(encoded_2)

    # Apply shared_layer_2_2 to encoded_3 and encoded_4
    encoded_7 = shared_layer_2_2(encoded_3)
    encoded_8 = shared_layer_2_2(encoded_4)

    # Apply shared_layer_1_3 to encoded_3 and encoded_4
    encoded_9 = shared_layer_1_3(encoded_5)
    encoded_10 = shared_layer_1_3(encoded_6)

    # Apply shared_layer_2_3 to encoded_3 and encoded_4
    encoded_11 = shared_layer_2_3(encoded_7)
    encoded_12 = shared_layer_2_3(encoded_8)

    # Compute the two distances
    distance_1 = Lambda(euclidean_distance, name='lambda_1')([encoded_9, encoded_10])
    distance_2 = Lambda(euclidean_distance, name='lambda_2')([encoded_11, encoded_12])
    
    # Concatenate the two sides of the model
    concat_layer = Concatenate(name='concatenation_layer')
    last_tensor = concat_layer([distance_1, distance_2])
    #output layer
    output_layer = Dense(units=3, activation='softmax', name='output_layer')
    output = output_layer(last_tensor)

    # Create Model with specified inputs and outputs
    model = Model(inputs=[rumor_input, user_input_name, user_input_description ], outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def model_with_ft(bert_model):

    MAX_LEN = 512  # Set your desired max length

    # Define input layers for text1
    input_ids1 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_ids1')
    attention_mask1 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='attention_mask1')
    token_type_ids1 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='token_type_ids1')

    # Get AraBert outputs for text1
    rumor_input = bert_model(input_ids1, attention_mask=attention_mask1, token_type_ids=token_type_ids1).last_hidden_state

    # Define input layers for text2
    input_ids2 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_ids2')
    attention_mask2 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='attention_mask2')
    token_type_ids2 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='token_type_ids2')

    # Get AraBert outputs for text2
    user_input_name = bert_model(input_ids2, attention_mask=attention_mask2, token_type_ids=token_type_ids2).last_hidden_state

    # Define input layers for text3
    input_ids3 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_ids3')
    attention_mask3 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='attention_mask3')
    token_type_ids3 = Input(shape=(MAX_LEN,), dtype=tf.int32, name='token_type_ids3')

    # Get AraBert outputs for text3
    user_input_description = bert_model(input_ids3, attention_mask=attention_mask3, token_type_ids=token_type_ids3).last_hidden_state

    # Define input shape for user_inputnumeric
    input_shape_numeric = (None, 2)

    # Create input layer with custom name for user_inputnumeric
    user_inputnumeric = Input(shape=input_shape_numeric, name='user_inputnumeric')


    # Create shared Dense layer 1 with 128 units and sigmoid activation
    shared_layer_1 = Dense(units=128, activation='sigmoid' , name='shared_layer_1')

    # Create shared Dense layer 2 with 128 units and sigmoid activation
    shared_layer_2 = Dense(units=128, activation='sigmoid', name='shared_layer_2')

    # Apply shared_layer_1 to rumor_input and user_input_name
    encoded_1_1 = shared_layer_1(rumor_input)
    encoded_2_1 = shared_layer_1(user_input_name) 


    # Compute the distance between the encoded vectors
    distance_1 = Lambda(euclidean_distance, name='lambda_1')([encoded_1_1, encoded_2_1])
    # Create shared Dense layer with 32 units and sigmoid activation
    dense_layer_1 = Dense(units=32, activation='sigmoid', name='dense_layer_1')
    encoded_distance_1 = dense_layer_1(distance_1)


    # Apply shared_layer_2 to rumor_input and user_input_description
    encoded_1_2 = shared_layer_2(rumor_input)
    encoded_2_2 = shared_layer_2(user_input_description)

    # Compute the distance between the encoded vectors
    distance_2 = Lambda(euclidean_distance, name='lambda_2')([encoded_1_2, encoded_2_2])
    # Create shared Dense layer with 32 units and sigmoid activation
    dense_layer_2 = Dense(units=32, activation='sigmoid', name='dense_layer_2')
    encoded_distance_2 = dense_layer_2(distance_2)


    # Concatenate the two sides of the model
    concat_layer = Concatenate(name='concatenation_layer')
    last_tensor = concat_layer([encoded_distance_1, encoded_distance_2])
    #output layer
    output_layer = Dense(units=3, activation='softmax', name='output_layer')
    output = output_layer(last_tensor)

    # Create Model with specified inputs and outputs
    model = tf.keras.models.Model(inputs=[input_ids1, attention_mask1, token_type_ids1 , input_ids2, attention_mask2, token_type_ids2 , input_ids3, attention_mask3, token_type_ids3], outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model




