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
	Institution string
	Level       string
	Award       string
	From        int8
	To          int8
}

type EmpHist struct {
	Institution string
	Position    string
	From        int8
	To          int8
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
	_, err := dbMap.Select(&profiles, "select * from swdata")

	if err != nil {
		log.Fatalf("Select statement failed -> %v", err.Error())
	}

	//	content := gin.H{}

	c.JSON(200, profiles)
}

func main() {
	dbMap = dbInit()
	app := gin.Default()
	app.GET("/profiles", getProfiles)
	app.GET("/profiles/:profile_id", getProfile)

	app.Run(":8080")
}
