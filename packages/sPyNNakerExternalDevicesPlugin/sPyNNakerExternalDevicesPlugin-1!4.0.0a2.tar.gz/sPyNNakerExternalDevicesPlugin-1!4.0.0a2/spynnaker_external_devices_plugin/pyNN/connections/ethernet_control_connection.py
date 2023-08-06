from spinn_front_end_common.utility_models.multi_cast_command \
    import MultiCastCommand

from spinnman.connections.udp_packet_connections.udp_eieio_connection \
    import UDPEIEIOConnection
from spinnman.messages.eieio.data_messages.eieio_data_message \
    import EIEIODataMessage
from spinnman.messages.eieio.data_messages.eieio_key_data_element \
    import EIEIOKeyDataElement
from spinnman.messages.eieio.data_messages.eieio_key_payload_data_element \
    import EIEIOKeyPayloadDataElement

from threading import Thread
import traceback


class EthernetControlConnection(UDPEIEIOConnection, Thread):
    """ A connection that can translate Ethernet control messages received\
        from a Population
    """

    def __init__(
            self, translator, local_host=None, local_port=None):
        """

        :param translator: The translator of multicast to control commands
        :param local_host: The optional host to listen on
        :param local_port: The optional port to listen on
        """
        UDPEIEIOConnection.__init__(
            self, local_host=local_host, local_port=local_port)
        Thread.__init__(
            self, name="Ethernet Control Connection on {}:{}".format(
                self.local_ip_address, self.local_port))
        self._translator = translator
        self._running = True
        self.setDaemon(True)
        self.start()

    def run(self):
        try:
            while self._running:
                eieio_message = self.receive_eieio_message()
                if isinstance(eieio_message, EIEIODataMessage):
                    while eieio_message.is_next_element:
                        element = eieio_message.next_element
                        if isinstance(element, EIEIOKeyDataElement):
                            self._translator.translate_control_packet(
                                MultiCastCommand(element.key))
                        elif isinstance(element, EIEIOKeyPayloadDataElement):
                            self._translator.translate_control_packet(
                                MultiCastCommand(element.key, element.payload))

        except Exception:
            if self._running:
                traceback.print_exc()

    def close(self):
        """ Close the connection
        """
        self._running = False
        UDPEIEIOConnection.close()
