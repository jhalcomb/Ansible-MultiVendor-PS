class FilterModule:

    @staticmethod
    def filters():
        return {"reform_vlans": FilterModule.reform_vlans}

    @staticmethod
    def reform_vlans(raw_vlans, strict_mode=False):
        """
        Converts the list of interfaces in each VLAN to the format required by
        the NAPALM validation by adding a 'list' key into the heirarchy, along
        with an optional '_mode' key for strict compliance checking.
        """
        new_vlans = {}
        napalm_vlans = raw_vlans["ansible_facts"]["napalm_vlans"]
        for vlan_id, vlan_attrs in napalm_vlans.items():

            # Perform a deep copy with all attrs first
            new_vlans.update({vlan_id: vlan_attrs})

            # Overwrite "interfaces" key with new structure
            new_vlans[vlan_id]["interfaces"] = {"list": vlan_attrs["interfaces"]}

            # Optionally add "_mode" key if strict mode is enabled
            if strict_mode:
                new_vlans[vlan_id]["interfaces"]["_mode"] = "strict"

        # Wrap the new VLAN dict in a list of dicts
        return [{"get_vlans": new_vlans}]
