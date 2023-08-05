"""Base class for learners in deepmodels.
"""

import abc
import tensorflow as tf

if tf.__version__ > "0.11":
  import tensorflow.contrib.slim as slim
else:
  import tensorflow.slim as slim

from deepmodels.tf.core import base_model


class DMLearner(object):
  """Base class for deepmodels learners.

  Attributes:
    input_tensor_name: name of input tensor, can be set to a custom name.
    output_tensor_name: name of output tensor.
    vars_to_train: variables to train.
    vars_to_restore: variables to restore from a model file.
    sess: tf.Session object to perserve a session for constant prediction.
  """
  __metaclass__ = abc.ABCMeta

  input_tensor_name = "inputs"
  output_tensor_name = "outputs"
  vars_to_train = None
  vars_to_restore = None
  sess = None
  dm_model = None

  def __init__(self):
    self.sess = tf.Session()

  def __del__(self):
    if self.sess is not None:
      self.sess.close()

  def check_dm_model_exist(self):
    """Check if dm_model exists.

    Enforce practice of using dm_model.
    """
    assert self.dm_model is not None, "dm_model can not be None"

  def set_dm_model(self, dm_model):
    """Use a dm model class.
    """
    self.dm_model = dm_model

  def set_key_vars(self, restore_scope_exclude, train_scopes):
    """Set critial variables for relevant tasks.

    Set vars_to_train and vars_to_restore.
    Called after build_model.

    Args:
      restore_scope_exclude: variable scopes to exclude for restoring.
      train_scopes: variable scopes to train.
    """
    self.vars_to_restore = slim.get_variables_to_restore(
        exclude=restore_scope_exclude)
    self.vars_to_train = []
    for scope in train_scopes:
      variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope)
      self.vars_to_train.extend(variables)
    if not self.vars_to_train:
      print "[set_key_vars: info] No variables to train were defined." \
            "Will train ALL variables."
      self.vars_to_train = None
    #base_model.print_variable_names(self.vars_to_train)

  def build_model(self, inputs):
    """Construct network graph using dm_model build_model().

    The internal input/output_tensor_name will be set based on
    dm_model.net_params.input/output_layer_name from endpoints.

    Args:
      inputs: input data, either data vectors or images.
    Returns:
      prediction and endpoints.
    """
    # why ismodel_params not used?
    self.check_dm_model_exist()
    outputs, endpoints = self.dm_model.build_model(inputs)
    if self.dm_model.net_params.input_layer_name != "":
      self.input_tensor_name = endpoints[
          self.dm_model.net_params.input_layer_name].name
    else:
      self.input_tensor_name = inputs.name
    if self.dm_model.net_params.output_layer_name != "":
      self.output_tensor_name = endpoints[
          self.dm_model.net_params.output_layer_name].name
    else:
      self.output_tensor_name = outputs.name
    return outputs, endpoints

  def get_output(self, input_data, preprocessed=True, target_tensor_name=""):
    """Get output from a specified tensor.

    Args:
      input_data: raw network input as numpy array.
      preprocessed: if the data has been preprocessed.
      target_tensor_name: target tensor to evaluate.
      Use internal output_tensor_name as default.
    Returns:
      evaluated tensor value.
    """
    self.check_dm_model_exist()
    if not preprocessed:
      input_data = self.dm_model.preprocess(input_data)
    if target_tensor_name == "":
      target_tensor_name = self.output_tensor_name
    return base_model.eval_tensor(self.sess, self.input_tensor_name,
                                  input_data, target_tensor_name)

  def load_model_from_checkpoint_fn(self, model_fn):
    """Load weights from file and keep in memory.

    Args:
      model_fn: saved model file.
    """
    if self.vars_to_restore is None:
      self.vars_to_restore = slim.get_variables()
    restore_fn = slim.assign_from_checkpoint_fn(model_fn, self.vars_to_restore)
    print "class session created."
    print "restoring model from {}".format(model_fn)
    restore_fn(self.sess)
    print "model restored."

  def load_model_from_pb(self, pb_fn):
    """Load model data from a binary protobuf file.

    Args:
      pb_fn: protobuf file.
    """
    pass
