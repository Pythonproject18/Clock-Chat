from CLOCK_CHAT.models import Reaction, MessageReaction


def get_message_reaction(message_id):
    try:
        reactions = MessageReaction.objects.filter(
            message=message_id, 
            is_active=True
        ).select_related('reacted_by', 'reaction')
        
        reaction_values = []
        for reaction in reactions:
            if reaction.reaction:  # Ensure reaction exists
                reaction_values.append({
                    'id': reaction.id,
                    'value': reaction.reaction.value,
                    'is_current_user': False,  # Will be set in view
                    'username': reaction.reacted_by.first_name if reaction.reacted_by else ''
                })
        return reaction_values
    except Exception as e:
        print(f"Error getting reactions: {e}")
        return []

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