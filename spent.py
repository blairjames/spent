#! /usr/bin/env python3

import aiohttp
import asyncio
import concurrent.futures
import aiofiles
import os
from typing import Generator, List


class Spencer:
    def __init__(self):
        self.domain: str = "https://impact.edu.au/"
        self.wordlist_path: str = os.getcwd() + "/sharepoint_list.txt"
        self.log_path: str = os.getcwd() + "/last_log.txt"

    async def read_list(self) -> Generator:
        file = open(self.wordlist_path, "r")
        lines = (f for f in file.readlines())
        file.close()
        return lines

    async def build_urls(self) -> List:
        try:
            paths = await self.read_list()
            paths = (p for p in paths if p)
            urls = [self.domain + p for p in paths]
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

    async def launch_reqests(self) -> List:
        try:
            urls = await self.build_urls()
            res = [await self.send_req(t) for t in urls]
            return [urls, res]
        except Exception as e:
            print("launch_requests: " + str(e))

    async def controller(self):
        try:
            res = await self.launch_reqests()
            urls = res[0]
            cont = res[1]
            cont = [c for c in cont]

            output = [("\n--------------------------------------------------------------------------------\n"
             "URL: " + u + " \n********* This data should not be visible to users *********\n" + i)
             for i in cont for u in urls
             if not "<p>HTTP Error 400. The request URL is invalid.</p>" in i]

            with open(self.log_path, "a") as file:
                file.writelines(output)
            [print(o) for o in output]

        except Exception as e:
            print("controller: " + str(e))

    def clear_log_file(self):
        try:
            with open(self.log_path, "w") as file:
                file.write("")
        except Exception as e:
            print("Error! in clear_log_file: " + str(e))

    def lint(self, input: str):
        print(input)
        with open(self.log_path, "a") as file:
            file.write(input + "\n")
            file.close()

    def present(self):
        os.system("clear")
        self.clear_log_file()
        self.lint("  ___  ___  ___  _ _  ___ ")
        self.lint(" / __>| . \| __>| \ ||_ _|")
        self.lint(" \__ \|  _/| _> |   | | | ")
        self.lint(" <___/|_|  |___>|_\_| |_| ")
        self.lint("\nSharePoint ENumeration Tool")
        self.lint("   spent@blairjames.com")
        self.lint("\nSource: git clone github.com/blairjames/spent")
        self.lint("\nProcessing requests..")


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
