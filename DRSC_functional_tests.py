#! /usr/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import sys, random

devel_mode = False # True if we are testing development site

def DRSC_URL(more = ''):
    if more and more[0] != '/':
        more = '/' + more
    if devel_mode:
        return "http://dev.www.flyrnai.org" + more
    else:
        return "http://www.flyrnai.org" + more


class GeneralTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.titles = {
            "DIOPT": "DRSC Integrative Ortholog Prediction Tool",
            "cellexpress":      "Gene Expression Levels by Cell Line",
            "TRiP":     "The Transgenic RNAi Resource Project",
            "DIOPTM":   "DRSC Integrative Ortholog Prediction Tool",
            "screensummary":    "Public DRSC Screens",
            "genelookup":       "Gene/Reagent Lookup",
            "DIOPT-DIST":       "Disease Gene Query",
            "TRiPstocks":       "Batch TRiP Stock Lookup",
            "snapdragon":       "SnapDragon - dsRNA Design",
            "heatmap":  "Heatmapped Data Display",
            "UP-TORR":  "UP-TORR",
            "HuDis":    "HuDis-TRiP",
            "minotar":  "MinoTar: MicroRNA ORF Target Predictions",
            "signedppi":        "SignedPPI",
            "FlyPrimerBank":    "DRSC FlyPrimerBank",
            "login":    "Member Login Page",
            "RNAi-rescue":      "Genes for RNAi Rescue",
            "HRMA":     "HRM",
            "TALEs":    "TALE Request",
            "RSVP":     "RNAi Stock Validation",
            # THIS LIST IS FAR FROM COMPLETE
            }

    def tearDown(self):
        self.browser.quit()

    def test_does_the_title_match_the_page_title(self):
        # standard question - is the page title correct for this page
        # (or did we forget to update it when we copied the code for
        # this page from somewhere else?)
        for page in (self.titles):
            self.browser.get(DRSC_URL(page))
            self.assertIn(self.title[page], self.browser.title)
            ## Perhaps a better test would be to crawl every link and
            ## assert that none of the pages have the same title?


class DIOPTTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.geneList = "nc\nng1\nng2\nwg\nDRSC05220\nDRSC06738\nDRSC27862\n" +\
            "JF02254\nDRSC07353\nDRSC27666\n\n\nCASP9\ncytochrome c\n" +\
            "APAF-1\nCASP8\nCASP6\nCASP2\nCASP3\n\nCG3038\nG9a\nCG13377\n" +\
            "cin\newg"

    def tearDown(self):
        self.browser.quit()

    def assertDIOPT():
        self.assertIn("DRSC Integrative Ortholog Prediction Tool",
                      self.browser.title,
                      "Should be on the DIOPT page but instead the title " +
                      'reads "%s".' % self.browser.title)

    def test_links_to_DIOPT(self):
        # confirm that we can get to DIOPT from home page, tools page, and menu
        # this one should really be generalized for all pages

        # from link on home page
        self.browser.get(DRSC_URL(""))
        self.browser.find_element_by_link_text("DIOPT").send_keys(Keys.ENTER)
        self.assertDIOPT()

        # from the tools page
        self.browser.get(DRSC_URL("DRSC-TOO.html"))
        self.browser.find_element_by_link_text("DIOPT").send_keys(Keys.ENTER)
        self.assertDIOPT()

        # from the menu bar
        self.browser.get(DRSC_URL("DRSC-PRR.html"))
        # hover over tools menu
        ActionChains(self.browser).move_to_element(onToolTop[0]).perform()
        # get the tools submenu element
        menuDiv = self.browser.find_element_by_css_selector(
            "div#menuDivTools.menuDiv")
        # click the DIOPT link in the submenu
        menuDiv.find_element_by_link_text("DIOPT").send_keys(Keys.ENTER)
        self.assertDIOPT()

    def start_search_by_gene(self):
        # Alice goes to the DIOPT query page
        self.browser.get(DRSC_URL("DIOPT"))

        # She looks up her genes (and settings) of interest
        inputElement = self.browser.find_element_by_name("gene_list")
        inputElement.send_keys("\n".join(self.geneList))
        if self.vectorList:
            checkboxes = self.browser.find_elements_by_name("vector_cb_grp")
            for cbx in checkboxes:
                val = cbx.get_attribute("value")
                if val in self.vectorList:
                    cbx.click()
        if self.prodStatusList:
            checkboxes = self.browser.find_elements_by_name(
                "prod_status_cb_grp")
            for cbx in checkboxes:
                label = cbx.find_element(By.XPATH, "..") # label is parent
                                                         # of cbx
                val = label.text
                if val in self.vectorList:
                    self.set_checkbox(cbx)
                else:
                    self.unset_checkbox(cbx)
        self.browser.find_element_by_name("submit").click()
        self.wait_for_TRiP_DB_Query_results_page()

    def test_are_the_weighted_scores_close_to_the_scores(self):
        # test because Treefam got left out of weighted score,
        # checking close to score instead of specific number in case
        # weights change

        # Larry goes to DIOPT and looks up arm
        self.browser.get(DRSC_URL("DIOPT"))
        self.browser.find_element_by_name("gene_list").send_keys("arm")
        self.browser.find_element_by_name("submit").click()
        
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located( (By.LINK_TEXT,
                                               "Submit another query.") ),
            "Timed out while waiting for DIOPT Results page (for arm)."
            )

        # he gets back a table of orthologs predictions
        resultsTable = self.browser.find_element_by_css_selector(
            "td#mbodytd center table")

        # the second row is the best match (CTNNB1)
        rows = resultsTable.find_elements_by_tag_name("tr")
        header = rows[0].find_elements_by_tag_name("th")
        row1 = rows[1].find_elements_by_tag_name("td")
        tdDict = {}
        for i in range(len(header)):
            tdDict[header[i].text] = row1[i].text
        self.assertEqual(tdDict["Human Symbol"], "CTNNB1")
        score = int(tdDict["Score"])
        weightedScore = float(tdDict["Weighted Score"])
        self.assertTrue(score + 1 > weightedScore and score - 1 < weightedScore,
                        "Score (%d) is not close to Weighted Score (%03f)" %
                        (score, weightedScore))



class HuDisTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_do_the_rsvp_links_work(self):
        # THIS IS A TERRIBLE TEST
        # It's fun to pick a different row for the test each time, but
        # the problem is that some of these TRiP ids really aren't
        # found in RSVP Search, so THE TEST FAILS SOME OF THE TIME,
        # even if the code we're testing is correct.  Not sure what
        # the fix is - is it a bug that HuDis and RSVP data don't
        # match?

        # A user visits the HuDis page
        self.browser.get(DRSC_URL("HuDis"))
        
        # there is a table with many rows of data about human disease genes
        HuDisTable = self.browser.find_element_by_id("HuDis")
        rows = HuDisTable.find_elements_by_tag_name("tr")
        self.assertTrue(len(rows) > 100)

        # one column is RSVP Data
        header = rows[0].find_elements_by_tag_name("th")
        rsvpDataColumn = -1
        huDisGeneColumn = -1
        for th in header:
            if "RSVP Data" == th.text:
                rsvpDataColumn = header.index(th)
            elif "Human disease gene" == th.text:
                huDisGeneColumn = header.index(th)
        self.assertNotEqual(rsvpDataColumn, -1)
        self.assertNotEqual(huDisGeneColumn, -1)

        # the line ids in that column are links that take the user to
        # the RSVP line page
        while True:
            randomRow = random.choice(rows[1:])
            cells = randomRow.find_elements_by_tag_name("td")
            if cells[huDisGeneColumn].text and cells[rsvpDataColumn].text:
                break
        huDisGeneName = cells[huDisGeneColumn].text
        rsvpLine = cells[rsvpDataColumn].text
        links = cells[rsvpDataColumn].find_elements_by_tag_name("a")
        self.assertTrue(len(links) > 0)
        links[0].click()
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,
                                               "table[width='704']") ),
            "Timed out while waiting for RSVP detail window for %s (%s)." %
            (rsvpLine, huDisGeneName)
            )
        titles = self.browser.find_elements_by_css_selector("h2.homeh1")
        self.assertNotEqual(0, len(titles),
                            "Title not found when expecting RSVP page for " +
                                "%s (gene was %s)." %
                            (rsvpLine, huDisGeneName))
        errMsg = "Page title " +\
            "(%s) not right for RSVP page for %s (gene was %s)." %\
            (titles[0].text, rsvpLine, huDisGeneName)
        self.assertNotEqual(-1, titles[0].text.find("TRiP.%s" % rsvpLine),
                            errMsg)





if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.lower() == "-d":
            devel_mode = True
            print "Devel Mode"
            sys.argv.remove(arg)
        elif arg.lower() == "-p":
            devel_mode = False
            print "Prod Mode"
            sys.argv.remove(arg)
    unittest.main()
