package main

import (
  "fmt"
  "os"
  "io"
  "bufio"
  "path/filepath"
  "encoding/csv"
  "strings"
  "strconv"
  "github.com/fogleman/gg"
)

type fichier struct {
    dim int
    colonne int
    ligne int
    path string
}

type cercle struct {
  id string
  x float64
  y float64
  r float64
  c1 int
  c2 int
  c3 int
  c_x0 float64
  c_y0 float64
  c_x1 float64
  c_y1 float64
  i1 int
  i2 int
  i3 int
}


func infoFile(path string) fichier {
  clean := strings.Replace(path, ".csv", "", -1)
  fragments := strings.Split(clean, "\\")
  fileFragment := strings.Split(fragments[len(fragments)-1], "-")

  valDim, err := strconv.Atoi(fragments[len(fragments)-3]);
  if(err !=  nil){
    fmt.Println("erreur sur la dimension !")
  }

  valLigne, err := strconv.Atoi(fileFragment[0]);
  if(err !=  nil){
    fmt.Println("erreur sur la ligne !")
  }

  valColonne, err := strconv.Atoi(fileFragment[1]);
  if(err !=  nil){
    fmt.Println("erreur sur la colonne !")
  }
  
  return fichier{
    dim: valDim,
    colonne: valColonne,
    ligne: valLigne,
    path: path}
}

func searchAllInfo(paths []string) []fichier {
  fileInfo := []fichier{}

  for _, file := range paths {
      info := infoFile(file)
      fileInfo = append(fileInfo, info)
  } 

  return fileInfo
}

func searchAllFiles(path string) []string {
  fileList := []string{}

  filepath.Walk(path, func(path string, f os.FileInfo, err error) error {
      fileInfo, err := os.Stat(path)
      if(!fileInfo.IsDir()) {
        fileList = append(fileList, path)
      }
      return nil
  })

  return fileList 
}


func stringToCircle(fragment []string) cercle {
  x, err := strconv.ParseFloat(fragment[2], 64);
  if(err !=  nil){
    fmt.Println("erreur x invalide")
  }

  y, err := strconv.ParseFloat(fragment[3], 64);
  if(err !=  nil){
    fmt.Println("erreur y invalide")
  }

  r, err := strconv.ParseFloat(fragment[4], 64);
  if(err !=  nil){
    fmt.Println("erreur r invalide")
  }

  c1, err := strconv.Atoi(fragment[5]);
  if(err !=  nil){
    fmt.Println("erreur c1 invalide")
  }

  c2, err := strconv.Atoi(fragment[6]);
  if(err !=  nil){
    fmt.Println("erreur c2 invalide")
  }


  c3, err := strconv.Atoi(fragment[7]);
  if(err !=  nil){
    fmt.Println("erreur c3 invalide")
  }

  c_x0, err := strconv.ParseFloat(fragment[8], 64);
  if(err !=  nil){
    fmt.Println("erreur c_x0 invalide")
  }


  c_y0, err := strconv.ParseFloat(fragment[9], 64);
  if(err !=  nil){
    fmt.Println("erreur c_y0 invalide")
  }


  c_x1, err := strconv.ParseFloat(fragment[10], 64);
  if(err !=  nil){
    fmt.Println("erreur c_x1 invalide")
  }

  c_y1, err := strconv.ParseFloat(fragment[11], 64);
  if(err !=  nil){
    fmt.Println("erreur c_y1 invalide")
  }

  i1, err := strconv.Atoi(fragment[12]);
  if(err !=  nil){
    fmt.Println("erreur c_y1 invalide")
  }

  i2, err := strconv.Atoi(fragment[13]);
  if(err !=  nil){
    fmt.Println("erreur c_y1 invalide")
  }

  i3, err := strconv.Atoi(fragment[14]);
  if(err !=  nil){
    fmt.Println("erreur c_y1 invalide")
  }

  return cercle{
    id : fragment[1],
    x : x,
    y : y,
    r : r,
    c1 : c1,
    c2 : c2,
    c3 : c3,
    c_x0 : c_x0,
    c_y0 : c_y0,
    c_x1 : c_x1,
    c_y1 : c_y1,
    i1 : i1,
    i2 : i2,
    i3 : i3}
}


func parseFile(file fichier) []cercle {
  csvFile, _ := os.Open(file.path)
  reader := csv.NewReader(bufio.NewReader(csvFile))
  fmt.Println(file.path)
  cercles := []cercle{}

  for {
    line, error := reader.Read()
    if error == io.EOF {
        break
    } else if error != nil {
        fmt.Println(error)
    }

    cercles = append(cercles, stringToCircle(line))
  }

  return cercles
}

func exists(path string) (bool) {
    _, err := os.Stat(path)
    if err == nil { return true }
    if os.IsNotExist(err) { return false }
    return true
}

func prepareFolder(f fichier) string {
  basePath := "c:/laragon/www/map/build/assets/output/"
  dimPath := basePath + strconv.Itoa(f.dim)
  lignePath := dimPath + "/" + strconv.Itoa(f.ligne)

  if(!exists(dimPath)) {
    os.MkdirAll(dimPath, 0777)
  }

  if(!exists(lignePath)) {
    os.MkdirAll(lignePath, 0777)
  }

  return lignePath
}

func placeText(c cercle, dc *gg.Context, x float64, y float64) {
  nbCaract := len(c.id)
  largeurCaract := (c.c_x1 - c.c_x0)/float64(nbCaract)
  size := ((1.9755*largeurCaract) -0.0127)

  if(size >= 10) {
    if err := dc.LoadFontFace("c:/laragon/www/map/build/assets/input/nasalization-rg.ttf", size); err != nil {
      panic(err)
    }

    width, height := dc.MeasureString(c.id)
    dc.SetRGB255(255, 255, 255)
    dc.DrawString(c.id, x - width/2, y + height/2)
    dc.Fill()
    fmt.Println("trace !")    
  }
}


func traceCercle(f fichier, cercles []cercle, quality int) {
    correctionX := f.colonne * 256 * quality
    correctionY := f.ligne * 256 * quality
    strColonne := strconv.Itoa(f.colonne)
    strLigne := strconv.Itoa(f.ligne)
    outputFile := prepareFolder(f) + "/" + strLigne + "-" + strColonne + ".png"
    
    dc := gg.NewContext(256*quality, 256*quality)
    dc.SetRGB255(0, 0, 0)
    dc.DrawRectangle(0,0,256*float64(quality),256*float64(quality))
    dc.Fill()

    for _, c := range cercles {
      x:= (c.x*float64(quality)) - float64(correctionX)
      y:= (c.y*float64(quality)) - float64(correctionY)
      dc.DrawCircle(x, y, c.r*float64(quality))

      if(f.dim == 0) {
        dc.SetRGB255(c.i1, c.i2, c.i3)
      } else {
        dc.SetRGB255(c.c1, c.c2, c.c3)
      }
      
      dc.Fill()

      placeText(c, dc, x, y)
    }
    
    dc.SavePNG(outputFile)
}


func main() {
  searchDir := "c:/laragon/www/map/build/assets/tempo/txt/1"
  fileList := searchAllFiles(searchDir)
  fileInfos := searchAllInfo(fileList)
  
  for _, value := range fileInfos {
    cercles := parseFile(value)
    traceCercle(value, cercles, 2)
  }
}






/*
"github.com/fogleman/gg"
func traceCercle(i int) {
    const S = 150
    dc := gg.NewContext(250, 250)

    for i:=0; i<10; i++ {
      iteration:= float64(i)
      x:= 100 + iteration*40
      y:= 100 + iteration*40
      dc.DrawCircle(x, y, 30)
      dc.SetRGB(100, 100, 100)
      dc.Fill()
    }

    dc.SetRGB(0, 0, 0)
    dc.DrawStringAnchored("Hello, world!", 100, S/2, 0.5, 0.5)
    dc.Fill()
    dc.SavePNG("out.png")  
}

func main() {
  for i:=0; i<1000; i++ {
    traceCercle(1)
    fmt.Printf("%v\n", i)
  }  
}
*/