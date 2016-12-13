                # self.voiceQ.task_done()
                
                # while len(bufferData) < 5:
                #     print "get data from voice qqqq"
                #     try:
                #         data = self.voiceQ.get()
                #         print "speak data: ", data
                #         bufferData.append(data)
                #     except Exception as e:
                #         break

                # while (len(bufferData) > 0):
              
                # data = self.voiceQ.get()
                
                # if len(self.faceCum) > 4:
                #     self.faceCum = self.faceCum[1:]
                # if len(self.smileCum) > 4:
                #     self.smileCum = self.smileCum[1:]

                # if int(data[0]) in [0, 1]:
                #     self.faceCum.append(int(data[0]))
                #     self.smileCum.append(int(data[1]))
                # else:

                # faceMean = np.mean(self.faceCum)
                # smileMean = np.mean(self.smileCum)

                # if  faceMean > .7:
                #     if smileMean > .7:
                #         print "say alien do not smile"
                #         system("say alien do not smile")
                #     elif smileMean < .3:
                #         print ("say alien go away")
                #         system("say alien go away")

    
                # elif faceMean < .3:
                #     if smileMean > .7:
                #         print("say James nice smile")
                #         system("say James nice smile")

                #     elif smileMean < .3:
                #         print "say hello James"
                #         system("say hello James")


                # data = self.voiceQ.get()
                # print "voice queue: ", data        
                # if data == "00":
                #     # print "alien"
                #     system("say go away! alien")
                # elif data == "01":
                #     # print "alien smiling"
                #     system("say do not smile! alien")
                # elif data == "10":
                #     # print "James smiling"
                #     system("say hello James")
                #     # system(self.getWeather())
                # elif data == "11":
                #     # print "James"
                #     system("say nice smile James")
                # else:
                #     pass

                # with self.voiceQ.mutex:
                #     self.voiceQ.clear()