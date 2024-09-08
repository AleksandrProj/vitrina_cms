from wagtail import blocks


class VacancyBlock(blocks.StructBlock):
    vacancies = blocks.PageChooserBlock(target_model="home.VacanciesPage", label="Вакансия")


class VacanciesBlock(blocks.StreamBlock):
    """
        Блок лучших вакансий
    """
    title = blocks.CharBlock(
        max_length=100,
        required=True,
        label="Заголовок блока"
    )
    vacancies = VacancyBlock(label="Добавить вакансию")

    class Meta:
        block_counts = {
            "title": {
                "max_num": 1
            },
            "vacancies": {
                "max_num": 10
            }
        }