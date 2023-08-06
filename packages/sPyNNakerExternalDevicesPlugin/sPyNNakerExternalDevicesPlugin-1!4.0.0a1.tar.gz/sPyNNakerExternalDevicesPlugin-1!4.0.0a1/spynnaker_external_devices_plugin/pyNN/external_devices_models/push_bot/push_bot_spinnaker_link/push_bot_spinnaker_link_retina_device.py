# pynn imports

from pacman.executor.injection_decorator import inject, supports_injection
from pacman.model.graphs.application.application_spinnaker_link_vertex \
    import ApplicationSpiNNakerLinkVertex
from spynnaker.pyNN.utilities import constants
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .abstract_push_bot_retina_device import AbstractPushBotRetinaDevice
from pacman.model.decorators.overrides import overrides


@supports_injection
class PushBotSpiNNakerLinkRetinaDevice(
        AbstractPushBotRetinaDevice, ApplicationSpiNNakerLinkVertex):

    def __init__(
            self, n_neurons, spinnaker_link_id, protocol, resolution,
            board_address=None, label=None):
        AbstractPushBotRetinaDevice.__init__(self, protocol, resolution)
        ApplicationSpiNNakerLinkVertex.__init__(
            self, spinnaker_link_id=spinnaker_link_id,
            n_atoms=resolution.value.n_neurons,
            board_address=board_address, label=label)

        # stores for the injection aspects
        self._graph_mapper = None
        self._routing_infos = None
        self._new_key_command = None

    @inject("MemoryGraphMapper")
    def graph_mapper(self, graph_mapper):
        self._graph_mapper = graph_mapper
        if self._routing_infos is not None:
            self._update_new_key_payload()

    @inject("MemoryRoutingInfos")
    def routing_info(self, routing_info):
        self._routing_infos = routing_info
        if self._graph_mapper is not None:
            self._update_new_key_payload()

    @property
    @overrides(AbstractPushBotRetinaDevice.start_resume_commands)
    def start_resume_commands(self):

        # Note this is not undefined, it is just a property so, it can't
        # be statically analysed
        commands = AbstractPushBotRetinaDevice\
            .start_resume_commands.fget(self)  # @UndefinedVariable

        # Update the commands with the additional one to set the key
        new_commands = list()
        for command in commands:
            if command.key == self._protocol.disable_retina_key:

                # This has to be stored so that the payload can be updated
                self._new_key_command = self._protocol.set_retina_key(0)
                new_commands.append(self._new_key_command)
            new_commands.append(command)
        return new_commands

    def _update_new_key_payload(self):
        vertex = list(self._graph_mapper.get_machine_vertices(self))[0]
        key = self._routing_infos.get_first_key_from_pre_vertex(
            vertex, constants.SPIKE_PARTITION_ID)
        self._new_key_command.payload = key
