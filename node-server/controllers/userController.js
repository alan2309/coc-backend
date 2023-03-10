const User = require("../models/userModel");
const bcrypt = require("bcrypt");

module.exports.login = async (req, res, next) => {
  try {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user)
      return res.json({ msg: "Incorrect Username or Password", status: false });
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid)
      return res.json({ msg: "Incorrect Username or Password", status: false });
    delete user.password;
    return res.json({ status: true, user });
  } catch (ex) {
    next(ex);
  }
};

module.exports.register = async (req, res, next) => {
  try {
    const { username, email, password } = req.body;
    const usernameCheck = await User.findOne({ username });
    if (usernameCheck)
      return res.json({ msg: "Username already used", status: false });
    const emailCheck = await User.findOne({ email });
    if (emailCheck)
      return res.json({ msg: "Email already used", status: false });
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({
      email,
      username,
      password: hashedPassword,
    });
    delete user.password;
    return res.json({ status: true, user });
  } catch (ex) {
    next(ex);
  }
};

module.exports.getAllUsers = async (req, res, next) => {
  try {
    const users = await User.find({ _id: { $ne: req.params.id } }).select([
      "email",
      "username",
      "avatarImage",
      "_id",
    ]);
    return res.json(users);
  } catch (ex) {
    next(ex);
  }
};
module.exports.addFriend = async (req, res, next) => {
  try {
    const { myemail, email } = req.body;
    await User.findOne({ email: email }, (err, doc) => {
      doc.friends.push(myemail);
      doc.save((e) => {
        console.log(e);
      });
    });
    await User.findOne({ email: myemail }, (err, doc) => {
      doc.friends.push(email);
      doc.save((e) => {
        console.log(e);
      });
    });
    return res.json("Success");
  } catch (ex) {
    next(ex);
  }
};
module.exports.getAllFrndsUsers = async (req, res, next) => {
  try {
    const users = await User.find({ _id: req.params.id }).select([
      "email",
      "username",
      "avatarImage",
      "friends",
      "_id",
    ]);
    let frndsArr = [];
    for (let x in users[0]["friends"]) {
      console.log(users[0]["friends"][x]);
      let frnd = await User.find({ email: users[0]["friends"][x] }).select([
        "email",
        "username",
        "avatarImage",
        "friends",
        "_id",
      ]);
      if (frnd !== null || frnd !== undefined) {
        frndsArr.push(frnd[0]);
      }
    }
    return res.json(frndsArr);
  } catch (ex) {
    next(ex);
  }
};

module.exports.setAvatar = async (req, res, next) => {
  try {
    const userId = req.params.id;
    const avatarImage = req.body.image;
    const userData = await User.findByIdAndUpdate(
      userId,
      {
        isAvatarImageSet: true,
        avatarImage,
      },
      { new: true }
    );
    return res.json({
      isSet: userData.isAvatarImageSet,
      image: userData.avatarImage,
    });
  } catch (ex) {
    next(ex);
  }
};

module.exports.logOut = (req, res, next) => {
  try {
    if (!req.params.id) return res.json({ msg: "User id is required " });
    onlineUsers.delete(req.params.id);
    return res.status(200).send();
  } catch (ex) {
    next(ex);
  }
};
