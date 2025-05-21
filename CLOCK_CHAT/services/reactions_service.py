from CLOCK_CHAT.models import Reaction, MessageReaction

def get_message_reaction(message_id):
    try:
        reactions = MessageReaction.objects.filter(
            message=message_id, 
            is_active=True
        ).select_related('reacted_by', 'reaction')

        grouped = {}
        for reaction in reactions:
            if not reaction.reaction:
                continue
            key = reaction.reaction.value
            if key not in grouped:
                grouped[key] = {
                    'value': key,
                    'count': 0,
                    'usernames': [],
                    'is_current_user': False,
                    'id': reaction.reaction.id  # using reaction_id as identifier
                }
            grouped[key]['count'] += 1
            grouped[key]['usernames'].append(reaction.reacted_by.first_name)
            if reaction.reacted_by:
                grouped[key]['is_current_user'] |= (reaction.reacted_by.id == reaction.created_by_id)

        return list(grouped.values())

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