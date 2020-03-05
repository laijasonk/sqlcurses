#!/usr/bin/env python3

import platform
import curses
import time
import sys
import os
from sqlalchemy import *


def init_scr():

    """ Initialize the curses window and return scr

    """

    scr = curses.initscr()

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.halfdelay(1)
    scr.keypad( True )
    scr.clear()

    return scr


def term_scr( scr ):
    
    """ User scr to terminate the window and revert back to terminal

    :param scr: Screen object from curses initscr

    """

    curses.nocbreak()
    scr.keypad( False )
    curses.echo()
    curses.endwin()


def check_term_size_change( scr, scr_dim ):

    """ Checks if change in window size
    
    :param scr: screen object from curses initscr
    :param scr_dim: dimensions to check
    :return: True for change, False for no change

    """

    if scr_dim != scr.getmaxyx():
        return True

    return False


def open_top_bar( scr_dim ):

    """ Create and return the top bar 

    :param scr_dim: dimensions of the screen
    :return: curses window object for the top bar

    """

    # format: curses.newwin(nlines, ncols, begin_y, begin_x)
    scr_top = curses.newwin( 4, scr_dim[1], 0, 0 )

    return scr_top

def open_front_main(scr_dim):

    scr_front_main = curses.newwin(scr_dim[0]-4, scr_dim[1], 4, 0)

    if scr_dim[1] > 64:
        scr_front_main.addstr(2, 2, "HELP:")
        scr_front_main.addstr(3, 2, "Make sure to open the database from the command line")
        scr_front_main.addstr(4, 2, "e.g. sqlcurses -t sqlite -d demo.sqlite3")
        scr_front_main.addstr(5, 2, "e.g. sqlcurses -t postgres -d demo -u johnsmith -h localhost")
        scr_front_main.addstr(5, 2, "e.g. sqlcurses -t mysql -d dev -u john -p pass -h devc -s /tmp/mysql.sock")
        scr_front_main.addstr(7, 2, "[h] Toggle help window")
        scr_front_main.addstr(8, 2, "[Arrows] Move around database")
        scr_front_main.addstr(9, 2, "[<>] Move between headers for each table")
        scr_front_main.addstr(10, 2, "[delete] Move back to table select")
        scr_front_main.addstr(11, 2, "[f] Find in database")
        scr_front_main.addstr(12, 2, "[n] New database entry or new execution")
        scr_front_main.addstr(13, 2, "[u] Update database entry")
        scr_front_main.addstr(14, 2, "[d] Delete database entry, cell or execution")
        scr_front_main.addstr(15, 2, "[k] Query mode")
        scr_front_main.addstr(16, 2, "[q] Quit")
        scr_front_main.addstr(17, 2, "[s] Save database")

        if scr_dim[0] > 25:
            scr_front_main.addstr(19, 2, "Thank you for using SQLcurses! This was made to allow SQL")
            scr_front_main.addstr(20, 2, "database manipulation to be done right in the console.")

    else:
        scr_front_main.addstr(2, 2, "HELP:")
        scr_front_main.addstr(3, 2, "Open from shell")
        scr_front_main.addstr(4, 2, "e.g. sqlcurses demo.sqlite3")
        scr_front_main.addstr(6, 2, "[h] Toggle help window")
        scr_front_main.addstr(7, 2, "[Arrows] Move around database")
        scr_front_main.addstr(8, 2, "[<>] Move between headers for each table")
        scr_front_main.addstr(9, 2, "[delete] Move back to table select")
        scr_front_main.addstr(10, 2, "[f] Find in database")
        scr_front_main.addstr(11, 2, "[n] New database entry or new execution")
        scr_front_main.addstr(12, 2, "[u] Update database entry")
        scr_front_main.addstr(13, 2, "[d] Delete database entry, cell or execution")
        scr_front_main.addstr(14, 2, "[k] Query mode")
        scr_front_main.addstr(15, 2, "[q] Quit")
        scr_front_main.addstr(16, 2, "[s] Save database")

    scr_front_main.border(0)

    return scr_front_main

def open_show_left(scr_dim):

    scr_show_left = curses.newwin(scr_dim[0]-4-3, 16, 4, 0)

    scr_show_left.border(0)

    return scr_show_left

def open_show_main(scr_dim):

    scr_show_main = curses.newwin(scr_dim[0]-4-3, scr_dim[1]-16, 4, 16)

    scr_show_main.border(0)

    return scr_show_main

def open_query_main(scr_dim):

    scr_query_main = curses.newwin(scr_dim[0]-4-3, scr_dim[1], 4, 0)

    scr_query_main.border(0)

    return scr_query_main

def open_bottom_bar(scr_dim):

    scr_bottom = curses.newwin(3, scr_dim[1], scr_dim[0]-3, 0)

    return scr_bottom

# refreshes each of the main windows
def refresh_windows(current_screen, scr_top, scr_front_main, scr_show_left, scr_show_main, scr_bottom, scr_query_main):

    if current_screen == 1:
        scr_top.refresh()
        scr_front_main.refresh()
    elif current_screen == 2:
        scr_top.refresh()
        scr_show_left.refresh()
        scr_show_main.refresh()
        scr_bottom.refresh()
    elif current_screen == 3:
        scr_top.refresh()
        scr_query_main.refresh()
        scr_bottom.refresh()
    else:
        scr_top.refresh()

# sets up .sqlcurses folder
def create_environment():

    root_path = os.path.expanduser("~")

    if not os.path.exists(root_path + "/.sqlcurses"):
        try:
            os.makedirs(root_path + "/.sqlcurses", exist_ok=True)
        except:
            os.makedirs(root_path + "/.sqlcurses")
        try:
            os.system("cp " + os.path.dirname(sqlcurses.__file__) + "/saved_databases " + root_path + "/.sqlcurses/saved_databases")
        except:
            pass

    if not os.path.isfile(root_path + "/.sqlcurses/saved_databases"):
        try:
            os.system("cp " + os.getcwd() + "/sqlcurses/saved_databases " + root_path + "/.sqlcurses/saved_databases")
        except:
            f = open(root_path + "/.sqlcurses/saved_databases", "a")
            auto_content = "# sqlcurses saved databases\n# Edit manually or save opened database via the app\n# Format:\n# db_short_name database_type:///username:password@host/dbname current_working_directory (for sqlite3)\n# e.g. dev postgresql://johnsmith:test123@localhost/dev_db\n# e.g. devtest sqlite:///devtest.db /home/johnsmith/dbfiles/test1"
            f.write(auto_content)
            f.close()


