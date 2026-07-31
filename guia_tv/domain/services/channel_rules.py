class ChannelRules:

    @staticmethod
    def can_be_featured(channel):

        return (
            channel.is_active
            and channel.is_public
        )

    @staticmethod
    def is_online(channel):

        return channel.status == "online"