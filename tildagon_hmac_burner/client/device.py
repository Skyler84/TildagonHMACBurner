import esptool
import espefuse

class ESP:
    def __init__(self, port=None):
        self.esp = esptool.get_default_connected_device(esptool.get_port_list(), port=port, connect_attempts=1, initial_baud=115200)

    def read_mac(self):
        mac_address = self.esp.read_mac("BASE_MAC")
        mac_str = '-'.join([f"{b:02X}" for b in mac_address])
        return mac_str

    def burn_hmac_key(self, hmac_key, key_to_use=1, do_not_confirm=False):
        commands = espefuse.init_commands(esp=self.esp, do_not_confirm=do_not_confirm)
        class Args:
            name_value_pairs = {}
        args = Args()
        args.name_value_pairs[f"KEY_PURPOSE_{key_to_use}"] = 8
        args.name_value_pairs[f"BLOCK_KEY{key_to_use}"] = hmac_key
        args.name_value_pairs[f"RD_DIS"] = (1<<(key_to_use))
        # args.name_value_pairs[f"WR_DIS"] = (1<<(23+key_to_use))
        commands.burn_efuse(args.name_value_pairs)
        