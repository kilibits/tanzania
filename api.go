package main

import (
	"database/sql"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"gopkg.in/gorp.v1"
)

type Profile struct {
	Name        string
	Group       string
	Area        string
	Phone       string
	Email       string
	Image       string
	Member_Type string
	Address     string
	Birth_Date  string
	Id          int
	Term        int
	Source      string
	// PoliticalExperience []PolHist
	// EducationHistory    []EduHist
	// EmploymentHistory   []EmpHist
}

type EduHist struct {
	Institution string
	Level       string
	Award       string
	From        int
	To          int
}

type EmpHist struct {
	Institution string
	Position    string
	From        int
	To          int
}

type PolHist struct {
	Institution string
	Position    string
	From        int
	To          int
}

func getProfile(c *gin.Context) {

}

var dbMap *gorp.DbMap

func dbInit() *gorp.DbMap {
	db, err := sql.Open("sqlite3", "scraperwiki.sqlite")
	if err != nil {
		log.Fatalf("Error Opening Database -> %v", err.Error())
	}

	dbMap := &gorp.DbMap{Db: db, Dialect: gorp.SqliteDialect{}}
	// dbMap.AddTableWithName(Profile{}, "swdata").SetKeys(true, "Id")
	// err = dbMap.CreateTablesIfNotExists()
	// if err != nil {
	// 	log.Fatalf("Failed to create table -> %v", err.Error())
	// }

	return dbMap
}

func getProfiles(c *gin.Context) {

	var profiles []Profile
	_, err := dbMap.Select(&profiles, "SELECT * FROM profile")

	if err != nil {
		log.Fatalf("Select statement failed -> %v", err.Error())
	}

	//	content := gin.H{}

	c.JSON(200, profiles)
}

func getEducationHistory(c *gin.Context) {
	var edu []EduHist
	name := c.Params.ByName("id")
	_, err := dbMap.Select(&edu, "SELECT schoolName, level, award, [from], [to] FROM profile JOIN education_history ON swdata.id = education_history.mp_id WHERE swdata.name LIKE '%?%'", name)

	if err != nil {
		log.Fatalf("Select statement failed -> %v", err.Error())
	}

	c.JSON(200, edu)
}

func main() {
	dbMap = dbInit()
	app := gin.Default()
	app.GET("/profiles", getProfiles)
	app.GET("/profiles/:profile_id", getProfile)
	app.GET("/education/:id", getEducationHistory)
	app.GET("/download", downloadImages)

	app.Run(":9000")
}

//Temporary function to download images and store them
//Stored images will then be stored on a CDN instead of calling from parliament site

//TODO: Add http request retries to avoid timeouts
func downloadImages(c *gin.Context) {

	var links []Profile
	_, err := dbMap.Select(&links, "SELECT id, image FROM profile")

	if err != nil {
		log.Fatalf("Select statement failed -> %v", err.Error())
	}

	for _, prof := range links {
		var _, err = os.Stat("./images/" + strconv.Itoa(prof.Id) + ".jpeg")

		if os.IsNotExist(err) {
			file, err := os.Create("./images/" + strconv.Itoa(prof.Id) + ".jpeg")
			if err != nil {
				log.Fatalf("Failed to create image -> %v", err.Error())
			}
			defer file.Close()

			response, err := http.Get(prof.Image)

			if err != nil {
				log.Fatalf("Unable to get url -> %v", err.Error())
			}

			defer response.Body.Close()

			io.Copy(file, response.Body)
		}
	}
}
