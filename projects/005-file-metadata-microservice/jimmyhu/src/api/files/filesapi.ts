const expr = require('express')
const fileUpload = require('express-fileupload')
const cors = require('cors')


const router = expr.Router()
router.use(cors())
router.use(fileUpload({
    createParentPath: true
}))

router.post('/', async (req:any, res: any) =>{
    let updatedFile = req.files.upfile
    let fileInfo = {
        "fileName" : updatedFile.name,
        "type": updatedFile.mimetype,
        "size": updatedFile.size,
    }
    res.json(fileInfo)
})  

module.exports = router