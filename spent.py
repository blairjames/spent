#! /usr/bin/env python3

import aiohttp
import asyncio
import os
from typing import Generator


class Spencer:
    def __init__(self):
        self.domain: str = "https://qed.qld.gov.au/"
        self.wordlist_path: str = os.getcwd() + "/sharepoint_list.txt"
        self.log_path: str = os.getcwd() + "/last_log.txt"

    async def read_list(self) -> Generator:
        file = open(self.wordlist_path, "r")
        lines = (f for f in file.readlines())
        file.close()
        return lines

    async def build_urls(self) -> Generator:
        try:
            paths = await self.read_list()
            paths = (p for p in paths if p)
            urls = (self.domain + p for p in paths)
            return urls
        except Exception as e:
            print("build_urls: " + str(e))

    async def send_req(self, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as res:
                    return await res.text()
        except Exception as e:
            print("send_req: " + str(e))

    async def launch_reqests(self):
        try:
            urls = await self.build_urls()
            res = [await self.send_req(t) for t in urls]
            return res
        except Exception as e:
            print("launch_requests: " + str(e))

    async def controller(self):
        try:
            finish = await self.launch_reqests()
            [print(f) for f in finish]
             #if not "<p>HTTP Error 400. The request URL is invalid.</p>" in f]

        except Exception as e:
            print("parse_response: " + str(e))

    def clear_log_file(self):
        try:
            with open(self.log_path, "w") as file:
                file.write("")
        except Exception as e:
            print("Error! in clear_log_file: " + str(e))

    def present(self):
        os.system("clear")
        self.clear_log_file()
        print(" ___  ___  ___  _ _  ___ ")
        print("/ __>| . \| __>| \ ||_ _|")
        print("\__ \|  _/| _> |   | | | ")
        print("<___/|_|  |___>|_\_| |_| ")
        print("\nSharePoint ENumeration Tool")
        print("\nProcessing requests..")

def main():
    try:
        spen = Spencer()
        loop = asyncio.get_event_loop()
        spen.present()
        task = loop.create_task(spen.controller())
        loop.run_until_complete(task)
    except Exception as e:
        print("main(): " + str(e))

if __name__ == '__main__':
    main()
