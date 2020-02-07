#! /usr/bin/env python
# coding: utf-8
import os
import os.path
import struct
import sys
import zipfile
import Utils

class zipmgr:
    def valid(self, filename):
        print("test")

    @staticmethod
    def unzip(apk_path, dst_path):
        if not zipfile.is_zipfile(apk_path):
            return False

        if not os.path.exists(dst_path):
            os.mkdir(dst_path, 0o777)

        zfobj = zipfile.ZipFile(apk_path)
        for name in zfobj.namelist():
            oriname = name
            if os.sep == '\\':
                name = name.replace('/', os.sep)
            if name.endswith(os.sep):
                Utils.create_dirs(os.path.join(dst_path, name))
                pass
            else:
                filepath = os.path.join(dst_path, name)
                dir = os.path.dirname(filepath)
               
                if not os.path.exists(dir):
                    Utils.create_dirs(dir)
         
                file = open(filepath, 'wb')
                file.write(zfobj.read(oriname))
                file.close()
        
        return True

    #读取APK文件名列表
    @staticmethod
    def getZipNameList(apk_path):
        zipnamelist = []
        if not zipfile.is_zipfile(apk_path):
            return []
        try:
            zfobj = zipfile.ZipFile(apk_path)
            zipnamelist = zfobj.namelist()
            zfobj.close()
        except Exception as e:
            print("%s" % e)
        finally:
            return zipnamelist

    #解压某个特定名称的文件, 解压一个dex, 如果dex大小超过30M， 认为是恶意apk, 将忽略
    @staticmethod
    def unzip_file(apk_path,filename,dst_path):

        if not zipfile.is_zipfile(apk_path):
            return None
        if not os.path.exists(dst_path):
            os.mkdir(dst_path, 0o777)
        filepath = ''
        try :
            zfobj = zipfile.ZipFile(apk_path)
            oriname = filename

            if os.sep == '\\':
                filename = filename.replace('/', os.sep)
            if filename.endswith(os.sep):
                Utils.create_dirs(os.path.join(dst_path, filename))
                pass
            else:
                apkname = os.path.splitext(os.path.basename(apk_path))[0]
                filepath = os.path.join(dst_path,apkname+'_'+filename)
                dir = os.path.dirname(filepath)
                if not os.path.exists(dir):
                    Utils.create_dirs(dir)
                fileinfo = zfobj.getinfo(oriname)
                if fileinfo.file_size > 30 * 1024 * 1024:
                    zfobj.close()
                    return None
                content = zfobj.read(oriname)
                zfobj.close()#即使在上面某些发生异常应该也没事，zfobj的析构函数会调用close
                with open(filepath, 'wb') as file:
                    file.write(content)
                return apkname+'_'+filename
        except:
            Utils.delete_file(filepath)
            return None

     #解压某个特定名称的文件, 解压一个dex, 如果dex大小超过30M， 认为是恶意apk, 将忽略
    @staticmethod
    def unzip_file_nocrete_dir(apk_path,filename,dst_path):

        if not zipfile.is_zipfile(apk_path):
            return None
        if not os.path.exists(dst_path):
            os.mkdir(dst_path, 0o777)
        filepath = ''
        try :
            zfobj = zipfile.ZipFile(apk_path)
            oriname = filename

            filename = filename.split('/')[-1]
            if filename.endswith(os.sep):
                Utils.create_dirs(os.path.join(dst_path, filename))
                pass
            else:
                apkname = os.path.splitext(os.path.basename(apk_path))[0]
                filepath = os.path.join(dst_path,apkname+'_'+filename)
                dir = os.path.dirname(filepath)
                if not os.path.exists(dir):
                    Utils.create_dirs(dir)
                fileinfo = zfobj.getinfo(oriname)
                if fileinfo.file_size > 30 * 1024 * 1024:
                    zfobj.close()
                    return None
                content = zfobj.read(oriname)
                zfobj.close()#即使在上面某些发生异常应该也没事，zfobj的析构函数会调用close
                with open(filepath, 'wb') as file:
                    file.write(content)
                return apkname+'_'+filename
        except:
            Utils.delete_file(filepath)
            return None

    @staticmethod
    def unzip_allIocn_to_dir(apk_path,filename,dst_path):

        if not zipfile.is_zipfile(apk_path):
            return False
        if not os.path.exists(dst_path):
            os.mkdir(dst_path, 0o777)
        filepath = ''
        try :
            zfobj = zipfile.ZipFile(apk_path)
            oriname = filename

            filename = filename.split('/')[-1]
            if filename.endswith(os.sep):
                Utils.create_dirs(os.path.join(dst_path, filename))
                pass
            else:
                apkname = os.path.splitext(os.path.basename(apk_path))[0]
                filepath = os.path.join(dst_path, apkname+'_'+filename)
                dir = os.path.dirname(filepath)
                if not os.path.exists(dir):
                    Utils.create_dirs(dir)

                for resFileName in zfobj.namelist():
                    if str(resFileName).startswith('res/', 0) and str(resFileName).endswith(filename):
                        # print resFileName
                        fileinfo = zfobj.getinfo(resFileName)
                        if fileinfo.file_size > 30 * 1024 * 1024:
                            continue

                        content = zfobj.read(resFileName)
                        with open(filepath, 'wb') as file:
                            file.write(content)
                            file.flush()

                        try:
                            dstfilePath = filepath
                            with open(filepath,'rb') as pngfile:
                                pngfile.seek(0x12,0)
                                pngSizeH = struct.unpack("B",pngfile.read(1))[0]
                                pngSizeL = struct.unpack("B",pngfile.read(1))[0]

                                size = pngSizeH*256+pngSizeL
                                # print size
                                length = len(dstfilePath)
                                type = dstfilePath[length-4:length]
                                dstfilePath = dstfilePath[0:length-4] +'_'+ str(size)+type
                            if not os.path.exists(dstfilePath):
                                os.rename(filepath, dstfilePath)
                            else:
                                Utils.delete_file(filepath)
                        except Exception as e1:
                            # print e1
                            pass
            zfobj.close()
            return True
        except Exception as e:
            Utils.delete_file(filepath)
            return False