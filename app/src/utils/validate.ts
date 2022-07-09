/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-04 13:37:50
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-09 14:21:29
 * @FilePath: /app/src/utils/validate.ts
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal (path: string): boolean {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
   * @param {string} str
   * @returns {Boolean}
   */
export function validUsername (str: string): boolean {
  return /^[a-zA-Z][a-zA-Z0-9_]{5,15}$/.test(str)
}
/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validPassword (str: string): boolean {
  return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,12}$/.test(str)
}
/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validPicCaptcha (str: string): boolean {
  return /^[A-Za-z0-9]{4}$/.test(str)
}
/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validEmail (str: string): boolean {
  return /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(str)
}
/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validEmailCaptcha (str: string): boolean {
  return /^[A-Za-z0-9]{6}$/.test(str)
}
/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validCUCUsername (str: string): boolean {
  return /^[1-9][0-9]{3,}$/.test(str)
}
