class BaseFilter:
    def _get_items_of_interest(self, details, keys):
        return dict((k, details[k]) for k in keys)


class StrictFilter(BaseFilter):
    def filter(self, inventory: dict):
        items_of_interest = {
            "general": ["name", "jamfBinaryVersion", "platform", "mdmCapable", "lastContactTime"],
            "diskEncryption": None,
            "localUserAccounts": None,
            "hardware": None,
            "operatingSystem": None
        }

        details = []

        for result in inventory["results"]:
            filtered_result = {}
            for item in items_of_interest.keys():
                if items_of_interest[item] is not None:
                    section = result[item]
                    filtered_section = self._get_items_of_interest(section, items_of_interest[item])
                else:
                    filtered_section = self._get_items_of_interest(result, [item])
                filtered_result[item] = filtered_section

            details.append(filtered_result)

        return details


class LooseFilter(BaseFilter):
    def filter(self, inventory: dict):
        items_of_interest = [
            "general",
            "diskEncryption",
            "localUserAccounts",
            "hardware",
            "operatingSystem"
        ]

        details = []

        for result in inventory["results"]:
            filtered_result = {}
            for item in items_of_interest:
                filtered_section = self._get_items_of_interest(result, [item])
                filtered_result[item] = filtered_section

            details.append(filtered_result)

        return details
