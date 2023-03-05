const {
  login,
  register,
  getAllUsers,
  addFriend,
  getAllFrndsUsers,
  setAvatar,
  logOut,
} = require("../controllers/userController");

const router = require("express").Router();

router.post("/login", login);
router.post("/register", register);
router.get("/getAllFrndsUsers/:id", getAllFrndsUsers);
router.post("/addFriend", addFriend);
router.get("/allusers/:id", getAllUsers);
router.post("/setavatar/:id", setAvatar);
router.get("/logout/:id", logOut);

module.exports = router;
