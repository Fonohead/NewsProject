# Проверка. Состоит ли текущий пользователь в группе authors.
def user_groups(request):
    if request.user.is_authenticated:
        has_authors_group = request.user.groups.filter(name='authors').exists()
    else:
        has_authors_group = False

    return {
        'user_has_authors_group': has_authors_group,

    }


def user_groups_context(request):
    # По умолчанию считаем, что пользователя нет в группах
    context = {
        'user_has_authors_group': False,
        'user_has_sub_politics_group': False,
        'user_has_sub_culture_group': False,
        'user_has_sub_sport_group': False,
        'user_has_sub_humour_group': False,
    }

    # Если пользователь авторизован, делаем один точный запрос в БД
    if request.user.is_authenticated:
        # Получаем все имена групп пользователя в виде списка строк
        user_groups = request.user.groups.values_list('name', flat=True)

        context['user_has_authors_group'] = 'authors' in user_groups
        context['user_has_sub_politics_group'] = 'sub_politics' in user_groups
        context['user_has_sub_culture_group'] = 'sub_culture' in user_groups
        context['user_has_sub_sport_group'] = 'sub_sport' in user_groups
        context['user_has_sub_humour_group'] = 'sub_humour' in user_groups

    return context