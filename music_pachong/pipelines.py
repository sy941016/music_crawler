# -*- coding: utf-8 -*-

import json
import os


class JsonPipeline:
    """将爬取结果以 JSON 格式逐行写入文件。"""

    def open_spider(self, spider):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "{}.json".format(spider.name))
        self.file = open(output_path, "w", encoding="utf-8")
        self.file.write("[\n")
        self._first_item = True
        spider.logger.info("Pipeline 已开启，结果将写入: {}".format(output_path))

    def close_spider(self, spider):
        self.file.write("\n]\n")
        self.file.close()
        spider.logger.info("Pipeline 已关闭，数据已保存。")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)
        if not self._first_item:
            self.file.write(",\n")
        self.file.write(line)
        self._first_item = False
        return item
