# Machine Learning Keras Suite
#
# A Python module that trains and evaluate an image classifier.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   15.09.2019
# Web:    https://github.com/bjoern-hempel/machine-learning-keras-suite
#
# LICENSE
#
# MIT License
#
# Copyright (c) 2019 Björn Hempel <bjoern@hempel.li>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
from mlks.commands.info.main import Info
from mlks.commands.prepare.main import Prepare
from mlks.commands.train.main import Train
from mlks.commands.demo.mnist.main import Mnist
from mlks.commands.demo.simple_perceptron.main import SimplePerceptron
from mlks.commands.demo.xor_perceptron.main import XorPerceptron
from mlks.commands.demo.nine_points.train.main import Train as NinePointsTrain
from mlks.commands.demo.nine_points.execute.main import Execute as NinePointsExecute
from mlks.helper.config import Config, DefaultChooser
from mlks.helper.config import general_config_writer, \
    machine_learning_config_writer, \
    transfer_learning_config_writer, \
    nine_points_config_writer
from mlks.helper.config import option_callback, add_options
from mlks.helper.config import set_config_translator


# Configure the universal parameters here
option_verbose = click.option(
    '--verbose', '-v',
    expose_value=False,
    is_flag=True,
    help='Switches the script to verbose mode.',
    callback=option_callback
)
option_debug = click.option(
    '--debug', '-d',
    expose_value=False,
    is_flag=True,
    help='Switches the script to debug mode.',
    callback=option_callback
)


# Configure the machine learning parameters here
option_epochs = click.option(
    '--epochs', '-e',
    cls=DefaultChooser,
    default_options={'default': 10, 'nine-points': 10000, 'mnist': 20},
    expose_value=False,
    is_flag=False,
    help='Sets the number of epochs.',
    callback=option_callback,
    default=DefaultChooser.get_default,
    type=int
)
option_learning_rate = click.option(
    '--learning-rate', '-l',
    expose_value=False,
    is_flag=False,
    help='Sets the learning rate.',
    callback=option_callback,
    default=0.001,
    type=float
)
option_activation_function = click.option(
    '--activation-function', '-a',
    expose_value=False,
    is_flag=False,
    help='Sets the activation function.',
    callback=option_callback,
    default='tanh',
    type=click.Choice(['tanh', 'sigmoid'])
)
option_loss_function = click.option(
    '--loss-function',
    expose_value=False,
    is_flag=False,
    help='Sets the loss function.',
    callback=option_callback,
    default='mean_squared_error',
    type=click.Choice(['mean_squared_error'])
)
option_optimizer = click.option(
    '--optimizer', '-o',
    expose_value=False,
    is_flag=False,
    help='Sets the optimizer.',
    callback=option_callback,
    default='adam',
    type=click.Choice(['adam'])
)
option_metrics = click.option(
    '--metrics',
    expose_value=False,
    is_flag=False,
    help='Sets the metrics.',
    callback=option_callback,
    default='accuracy',
    type=click.Choice(['accuracy'])
)
option_model_path = click.option(
    '--model-path',
    expose_value=False,
    is_flag=False,
    help='Sets the model path where the file can be saved.',
    default='-',
    type=click.File('w')
)


# Configure the transfer learning parameters here
option_transfer_learning_model = click.option(
    '--transfer-learning-model', '-m',
    expose_value=False,
    is_flag=False,
    help='Sets the transfer learning model.',
    callback=option_callback,
    default='Resnet52',
    type=str
)
option_number_trainable_layers = click.option(
    '--number-trainable-layers',
    expose_value=False,
    is_flag=False,
    help='Sets the number trainable layers.',
    callback=option_callback,
    default=3,
    type=int
)

# some other parameters here
option_x_0_1 = click.option(
    '--x',
    expose_value=False,
    is_flag=False,
    help='Sets a x value.',
    callback=option_callback,
    default=0.0,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_y_0_1 = click.option(
    '--y',
    expose_value=False,
    is_flag=False,
    help='Sets a y value.',
    callback=option_callback,
    default=0.0,
    type=click.FloatRange(min=0, max=1, clamp=False)
)


# Configure some option sets
option_set_general = [
    option_verbose,
    option_debug
]
option_set_machine_learning = [
    option_epochs,
    option_learning_rate,
    option_activation_function,
    option_loss_function,
    option_optimizer,
    option_metrics
]
option_set_transfer_learning = [
    option_transfer_learning_model,
    option_number_trainable_layers
]
option_set_nine_points = [
    option_x_0_1,
    option_y_0_1
]


# sets the config translator
set_config_translator({
    # general config
    'verbose': general_config_writer,
    'debug': general_config_writer,

    # machine learning config
    'epochs': machine_learning_config_writer,
    'learning_rate': machine_learning_config_writer,
    'activation_function': machine_learning_config_writer,
    'loss_function': machine_learning_config_writer,
    'optimizer': machine_learning_config_writer,
    'metrics': machine_learning_config_writer,
    'model_path': machine_learning_config_writer,

    # transfer learning config
    'transfer_learning_model': transfer_learning_config_writer,
    'number_trainable_layers': transfer_learning_config_writer,

    # some other configs
    'x': nine_points_config_writer,
    'y': nine_points_config_writer
})


# Make pass decorator for class Config
pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(name='cli')
@add_options(option_set_general)
def cli():
    """This scripts prepares, trains and validates an image classifier."""

    pass


@cli.command(name='prepare')
@add_options(option_set_general)
@click.option('--string', default='World', type=click.STRING, help='This is a string.')
@click.option('--repeat', default=1, type=click.INT, show_default=True, help='This is a integer.')
@click.argument('out', default='-', type=click.File('w'), required=False)
@pass_config
def cli_prepare(config, string, repeat, out):
    """This subcommand trains a classifier."""

    prepare_class = Prepare(config, string, repeat, out)
    prepare_class.do()


@cli.command(name='train')
@add_options(option_set_transfer_learning)
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_train(config):
    """This subcommand trains a classifier."""

    train_class = Train(config)
    train_class.do()


@cli.group(name='demo')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo(config):
    """This subcommand contains some demo examples."""

    pass


@cli_demo.command(name='simple-perceptron')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo_simple_perceptron(config):
    """This subcommand from demo trains a simple perceptron."""

    demo_class = SimplePerceptron(config)
    demo_class.do()


@cli_demo.command(name='xor-perceptron')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo_xor_perceptron(config):
    """This subcommand from demo trains a xor perceptron."""

    demo_class = XorPerceptron(config)
    demo_class.do()


@cli_demo.group(name='nine-points')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@add_options(option_set_nine_points)
@pass_config
def cli_demo_nine_points(config):
    """This subcommand from demo trains or execute a nine point example."""

    pass


@cli_demo_nine_points.command(name='train')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@add_options(option_set_nine_points)
@pass_config
def cli_demo_nine_points_train(config):
    """This subcommand from demo trains a nine point example."""

    demo_class = NinePointsTrain(config)
    demo_class.do()


@cli_demo_nine_points.command(name='execute')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@add_options(option_set_nine_points)
@pass_config
def cli_demo_nine_points_execute(config):
    """This subcommand from demo execute a nine point example."""

    demo_class = NinePointsExecute(config)
    demo_class.do()


@cli_demo.command(name='mnist')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo_mnist(config):
    """This subcommand from demo trains a mnist database."""

    demo_class = Mnist(config)
    demo_class.do()


@cli.command(name='info')
@add_options(option_verbose)
@pass_config
def cli_info(config):
    """This subcommand shows some infos."""

    info_class = Info(config)
    info_class.print()
