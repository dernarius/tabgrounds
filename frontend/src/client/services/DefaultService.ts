/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdvanceResult } from '../models/AdvanceResult';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DefaultService {
    /**
     * Read Root
     * Health check and status endpoint.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readRootGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }
    /**
     * Advance Game
     * Attempts to advance the game to the next stage.
     * @returns AdvanceResult Successful Response
     * @throws ApiError
     */
    public static advanceGameAdvancePost(): CancelablePromise<AdvanceResult> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/advance',
        });
    }
}
