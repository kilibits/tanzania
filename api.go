package main

import (
	"database/sql"
	"log"

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
	ID          int16
	Term        int16
	Source      string
	// PoliticalExperience []PolHist
	// EducationHistory    []EduHist
	// EmploymentHistory   []EmpHist
}

type EduHist struct {
	SchoolName string
	Level      string
	Award      string
	From       int16
	To         int16
}

type EmpHist struct {
	Institution string
	Position    string
	From        int16
	To          int16
}

type PolHist struct {
	Institution string
	Position    string
	From        int8
	To          int8
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
	_, err := dbMap.Select(&profiles, "SELECT * FROM swdata")

	if err != nil {
		log.Fatalf("Select statement failed -> %v", err.Error())
	}

	//	content := gin.H{}

	c.JSON(200, profiles)
}

func getEducationHistory(c *gin.Context) {
	var edu []EduHist
	name := c.Params.ByName("id")
	_, err := dbMap.Select(&edu, "SELECT schoolName, level, award, [from], [to] FROM swdata JOIN education_history ON swdata.id = education_history.mp_id WHERE swdata.name LIKE '%?%'", name)

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

	app.Run(":8080")
}
