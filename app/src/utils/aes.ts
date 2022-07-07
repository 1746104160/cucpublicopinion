/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-08 00:35:01
 * @FilePath: /app/src/utils/aes.ts
 */

/** *
 * @description aes加密 解密
 * @param { String } word 加密或解密的值
 * @param { String } keyStr 秘钥key
 * @returns { String} 返回值
 *
 */
import CryptoES from 'crypto-es'
import Cookies from 'js-cookie'
// 加密
export function encrypt (word:string) {
  const keyStr = Cookies.get('requestid') as string
  const key = CryptoES.enc.Utf8.parse(keyStr.slice(0, 32))
  const srcs = CryptoES.enc.Utf8.parse(word)
  const encrypted = CryptoES.AES.encrypt(srcs, key, { mode: CryptoES.mode.ECB, padding: CryptoES.pad.Pkcs7 })
  return encrypted.toString()
}
