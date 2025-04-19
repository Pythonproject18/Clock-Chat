from CLOCK_CHAT.models import Reaction, MessageReaction


def get_message_reaction(message_id):
    reactions = MessageReaction.objects.filter(message=message_id, is_active=True).values('id', 'reaction')
    
    reaction_values = []
    if reactions:  # This should be checking `reactions`, not `reaction_values`
        reaction_values = [
            {
                'id': reaction['id'],
                'value': get_reaction_value(reaction['reaction'])  # Use `reaction`, not `id` here
            }
            for reaction in reactions
        ]
    return reaction_values  # Don't forget to return it!

def get_reaction_value(reaction_id):
    reaction = Reaction.objects.filter(id=reaction_id, is_active=True).first()
    return reaction.value if reaction else None

def get_all_emojies():
    emojies= Reaction.objects.all()
    emojies_data=[]
    if emojies :
        emojies_data = [
            {
                'id' : emoji.id,
                'value' : emoji.value
            }
            for emoji in emojies
        ]
    print(emojies_data)    
    return emojies_data