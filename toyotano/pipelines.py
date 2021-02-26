import re
import sqlite3


class ToyotanoPipeline:
    conn = sqlite3.connect('toyotano.db')
    cursor = conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `toyotano` (
                                                                        title varchar(100),
                                                                        description text
                                                                        )''')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            title = item['title']
            title = re.sub('"', "'", title).strip()
        except:
            title = ''
        try:
            description = item['description']
            description = re.sub('"', "'", description).strip()
        except:
            description = ''

        self.cursor.execute(f'''select * from toyotano where description = "{description}"''')
        is_exist = self.cursor.fetchall()

        if len(is_exist) == 0:
            self.cursor.execute(
                f'''insert into `toyotano` (`title`, `description`) values ("{title}", "{description}")''')
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
