from app.models.lesson import LessonSection, PracticeTask


def save_lesson_content(db, lesson, sections_data):
    db.query(LessonSection).filter(LessonSection.lesson_id == lesson.id).delete()

    for s_data in sections_data:
        s_dict = s_data if isinstance(s_data, dict) else s_data.model_dump()

        is_practice = s_dict.get("type") == "practice"
        new_section = LessonSection(
            lesson_id=lesson.id,
            type=s_dict.get("type"),
            title=s_dict.get("title"),
            order_index=s_dict.get("order_index", 0),
            content=None if is_practice else s_dict.get("content"),
        )
        db.add(new_section)
        db.flush()

        if is_practice:
            for t_data in s_dict.get("tasks", []):
                t_dict = t_data if isinstance(t_data, dict) else t_data.model_dump()
                new_task = PracticeTask(
                    section_id=new_section.id,
                    task_type=t_dict.get("task_type", "code_check"),
                    title=t_dict.get("title"),
                    description=t_dict.get("description"),
                    order_index=t_dict.get("order_index", 0),
                    config=t_dict.get("config", {}),
                )
                db.add(new_task)