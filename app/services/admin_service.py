from app.models.lesson import Lesson, LessonSection, PracticeTask

def save_lesson_content(db, lesson, sections_data):
    db.query(LessonSection).filter(LessonSection.lesson_id == lesson.id).delete()

    for s_data in sections_data:
        s_dict = s_data if isinstance(s_data, dict) else s_data.model_dump()

        content_data = s_dict.get("content") or s_dict.get("props") or {}

        new_section = LessonSection(
            lesson_id=lesson.id,
            type=s_dict.get("type"),
            title=content_data.get("title", s_dict.get("type")),
            order_index=s_dict.get("order_index", 0),
            content=content_data
        )
        db.add(new_section)
        db.flush()


        if s_dict.get("type") == "practice":
            tasks_data = content_data.get("codingTasksProps", {}).get("tasks", [])

            for t_idx, t_data in enumerate(tasks_data):
                new_task = PracticeTask(
                    section_id=new_section.id,
                    task_type="code_check",
                    title=t_data.get("title"),
                    description=t_data.get("description"),
                    order_index=t_idx,
                    config=t_data
                )
                db.add(new_task)