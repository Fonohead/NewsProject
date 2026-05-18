# Проверка. Состоит ли текущий пользователь в группе authors.
def user_groups(request):
    if request.user.is_authenticated:
        has_authors_group = request.user.groups.filter(name='authors').exists()
    else:
        has_authors_group = False

    return {
        'user_has_authors_group': has_authors_group,
    }