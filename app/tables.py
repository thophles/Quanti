from db import *

db.init_app(app)
with app.app_context():
    db.session.add(
        Classes(name='Large-Format Camera', department='Photography',
        description="This course introduces students to ideas and attitudes that are inherent and possible with the large-format camera. The course covers traditional uses of large-format equipment including portraiture, landscapes, still life, and architecture, while developing a more personal viewpoint. The coursework covers sheet film, the zone system, printing skills, related equipment, and individual projects using the large-format image. Available for use are 4x5 and 8x10 view cameras. Students are required to have their own light meters.",
        semester='Spring 2018', teacher_one='28')
    ); db.session.commit()
